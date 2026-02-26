// =============================
// UI ELEMENTS
// =============================
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const statusBox = document.getElementById('statusBox');
const statusText = document.getElementById('statusText');
const statusMsg = document.getElementById('statusMsg');
const logEl = document.getElementById('log');

// =============================
// CONFIGURATION & STATE
// =============================

// Audio configuration
const TARGET_RATE = 24000;
const CHUNK_DURATION_MS = 150;
const MAX_LOG_LINES = 250;

// Connection state
let eventSource = null;
let wsAudio = null;
let stopped = false;

// Audio capture state
let micStream = null;
let audioContext = null;
let processorNode = null;
let capturing = false;
let pendingFloat = [];
let inputSampleRate = 48000;

// Audio playback state
let nextPlayTime = 0;
let suspendPlayback = false;
let assistantSources = [];

// UI state
let readySince = null;

function log(msg, level='info', obj){
  const line = document.createElement('div');
  line.className = level === 'error' ? 'err' : level === 'debug' ? 'dbg' : level === 'warn' ? 'warn' : '';
  const ts = new Date().toISOString().split('T')[1].replace('Z','');
  line.textContent = `[${ts} ${level}] ${msg}`;
  if(obj) {
    line.title = typeof obj === 'string' ? obj : JSON.stringify(obj).slice(0,300);
  }
  logEl.appendChild(line);
  while(logEl.children.length > MAX_LOG_LINES) logEl.removeChild(logEl.firstChild);
  logEl.scrollTop = logEl.scrollHeight;
}

function updateStatusUI(data){
  if(!data) return;
  statusText.textContent = data.state;
  statusMsg.textContent = data.message || '';
  const s = data.state;
  let colorVar = 'var(--c-status-idle)';
  if(['starting','processing'].includes(s)) colorVar = 'var(--c-status-processing)';
  else if(s === 'assistant_speaking') colorVar = 'var(--c-status-speaking)';
  else if(s === 'listening') colorVar = 'var(--c-status-listening)';
  else if(s === 'error') colorVar = 'var(--c-status-error)';
  else if(s === 'ready') colorVar = 'var(--c-status-ready)';
  else if(s === 'stopped') colorVar = 'var(--c-status-stopped)';
  statusBox.style.background = colorVar;
  if(s === 'stopped' || s === 'idle' || s === 'error') {
    stopMicCapture();
    stopBtn.disabled = true;
    startBtn.disabled = false;
    startBtn.textContent = 'Start Session';
  }
  if(s === 'ready') {
    if(!readySince) readySince = performance.now();
  } else {
    readySince = null;
  }
  if(s === 'ready' && !capturing && !stopped) {
    startMicCapture().catch(e=>log('Mic capture failed: '+e,'error'));
  }
}
// Gentle nudge: if still Ready after 3s and user hasn't spoken (no transition to listening), remind them
setInterval(()=>{
  if(readySince && (performance.now() - readySince) > 3000 && statusText.textContent === 'ready') {
    if(!statusMsg.textContent.includes('Speak')) {
      statusMsg.textContent = 'Ready – start speaking now.';
    }
  }
}, 1000);

// =============================
// SSE HANDLING
// =============================
function openEventSource(){
  if(eventSource){ eventSource.close(); }
  eventSource = new EventSource('/events');
  eventSource.onmessage = handleSSEMessage;
  eventSource.onerror = () => log('SSE connection error (will retry if closed).','warn');
  log('SSE connection opened');
}

function handleSSEMessage(ev) {
  if(!ev.data) return;
  
  try {
    const data = JSON.parse(ev.data);
    
    switch(data.type) {
      case 'status':
        handleStatusUpdate(data);
        break;
      case 'audio':
        handleAudioData(data);
        break;
      case 'log':
        log(data.msg || data.event_type || JSON.stringify(data), data.level || 'info');
        break;
      case 'control':
        handleControlEvent(data);
        break;
    }
  } catch(e){
    log('Bad SSE message: '+ e,'error');
  }
}

function handleStatusUpdate(data) {
  updateStatusUI(data);
  
  // Resume playback when assistant starts new response or reaches ready
  if(data.state === 'ready' || data.state === 'assistant_speaking') {
    if(suspendPlayback) {
      log('Resuming assistant playback (' + data.state + ')','debug');
      suspendPlayback = false;
    }
  }
}

function handleAudioData(data) {
  if(suspendPlayback) {
    return; // Drop audio while playback suspended
  }
  playAssistantPcm16(data.audio);
}

function handleControlEvent(data) {
  if(data.action === 'stop_playback'){
    try { stopAllAssistantPlayback(); } catch(_){ }
    suspendPlayback = true;
    log('Received stop_playback control from server; suspending playback until ready','debug');
  }
}

// =============================
// AUDIO CAPTURE & ENCODE
// =============================

function openAudioWebSocket(){
  try{
    const wsUrl = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.hostname + ':8765/ws-audio';
    wsAudio = new WebSocket(wsUrl);
    wsAudio.binaryType = 'arraybuffer';
    wsAudio.onopen = () => log('Audio websocket opened','debug');
    wsAudio.onerror = (e) => { log('Audio websocket error','warn'); wsAudio = null; };
    wsAudio.onclose = () => { log('Audio websocket closed','debug'); wsAudio = null; };
  }catch(e){ wsAudio = null; }
}
function ensureAudioContext(){
  if(!audioContext){
    audioContext = new (window.AudioContext || window.webkitAudioContext)({sampleRate: 48000});
    inputSampleRate = audioContext.sampleRate;
    nextPlayTime = audioContext.currentTime;
  }
}

async function startMicCapture(){
  if(capturing) return;
  ensureAudioContext();
  log('Requesting microphone…');
  micStream = await navigator.mediaDevices.getUserMedia({audio: { echoCancellation:true, noiseSuppression:true, channelCount:1 }, video:false});
  const source = audioContext.createMediaStreamSource(micStream);
  const BUFFER_SIZE = 4096; // 4096 / 48000 ~= 85ms
  processorNode = audioContext.createScriptProcessor(BUFFER_SIZE, 1, 1);
  let lastSend = performance.now();
  processorNode.onaudioprocess = (ev) => {
    if(!capturing) return;
    const input = ev.inputBuffer.getChannelData(0);
    pendingFloat.push(new Float32Array(input));
    const now = performance.now();
      // Send every CHUNK_DURATION_MS or if backlog large
    if(now - lastSend >= CHUNK_DURATION_MS || pendingFloat.length > 12){
      flushPendingAudio();
      lastSend = now;
    }
  };
  source.connect(processorNode);
  processorNode.connect(audioContext.destination); // required for some browsers
  capturing = true;
  log('Microphone capture started');
}

function stopMicCapture(){
  if(!capturing) return;
  capturing = false;
  if(processorNode){ try { processorNode.disconnect(); } catch(_){} }
  if(micStream){
    micStream.getTracks().forEach(t=>t.stop());
    micStream = null;
  }
  pendingFloat = [];
  log('Microphone capture stopped');
}

function mergePendingFloat(){
  if(!pendingFloat.length) return null;
  let total = 0;
  for(const arr of pendingFloat) total += arr.length;
  const merged = new Float32Array(total);
  let offset=0;
  for(const arr of pendingFloat){ merged.set(arr, offset); offset += arr.length; }
  pendingFloat = [];
  return merged;
}

function downsampleToInt16(float32, inRate, outRate){
  if(!float32) return null;
  if(inRate === outRate){
    const int16 = new Int16Array(float32.length);
    for(let i=0;i<float32.length;i++){
      const s = Math.max(-1, Math.min(1, float32[i]));
      int16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
    }
    return int16;
  }
  // Linear interpolation resampling for better quality than nearest-sample
  const ratio = inRate / outRate;
  const newLen = Math.round(float32.length / ratio);
  const int16 = new Int16Array(newLen);
  for (let i = 0; i < newLen; i++) {
    const srcPos = i * ratio;
    const idx = Math.floor(srcPos);
    const frac = srcPos - idx;
    let s1 = float32[idx] || 0;
    let s2 = float32[idx + 1] || 0;
    const sample = s1 * (1 - frac) + s2 * frac;
    const clamped = Math.max(-1, Math.min(1, sample));
    int16[i] = clamped < 0 ? clamped * 0x8000 : clamped * 0x7FFF;
  }
  return int16;
}

function int16ToBase64(int16){
  if(!int16) return null;
  const bytes = new Uint8Array(int16.buffer);
  let binary='';
  for(let i=0;i<bytes.length;i++) binary += String.fromCharCode(bytes[i]);
  return btoa(binary);
}

function flushPendingAudio(){
  const merged = mergePendingFloat();
  if(!merged || !merged.length) return;
  const int16 = downsampleToInt16(merged, inputSampleRate, TARGET_RATE);
  if(!int16) return;
  // Prefer binary websocket if available
  try{
    if(wsAudio && wsAudio.readyState === WebSocket.OPEN){
      // Int16Array underlying buffer is an ArrayBuffer of little-endian PCM16
      wsAudio.send(int16.buffer);
      return;
    }
  }catch(e){ /* fallthrough to HTTP fallback */ }
  const b64 = int16ToBase64(int16);
  if(!b64) return;
  sendAudioChunk(b64);
}

async function sendAudioChunk(b64){
  try {
    const r = await fetch('/audio-chunk', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({audio: b64}) });
    if(!r.ok){
      if(r.status === 400) {
        log('Audio chunk rejected: '+ r.status,'warn');
      } else {
        log('Audio send failed: '+ r.status,'warn');
      }
    }
  } catch(e){
    log('Audio send error: '+ e, 'warn');
  }
}

// Flush any straggling audio periodically (safety)
setInterval(()=>{ if(capturing) flushPendingAudio(); }, 500);

// =============================
// ASSISTANT AUDIO PLAYBACK
// =============================
function playAssistantPcm16(b64){
  try {
    ensureAudioContext();
    const binary = atob(b64);
    const bytes = new Uint8Array(binary.length);
    for(let i=0;i<binary.length;i++) bytes[i] = binary.charCodeAt(i);
    const view = new DataView(bytes.buffer);
    const samples = view.byteLength / 2;
    const floatBuf = new Float32Array(samples);
    for(let i=0;i<samples;i++){
      const s = view.getInt16(i*2, true) / 0x8000; // little-endian
      floatBuf[i] = s;
    }
    const audioBuf = audioContext.createBuffer(1, floatBuf.length, TARGET_RATE);
    audioBuf.copyToChannel(floatBuf, 0, 0);
    const src = audioContext.createBufferSource();
    src.buffer = audioBuf;
    src.connect(audioContext.destination);
    // track source so we can stop immediately on interrupt
    assistantSources.push(src);
    src.addEventListener('ended', () => {
      const i = assistantSources.indexOf(src);
      if(i !== -1) assistantSources.splice(i,1);
    });
    const now = audioContext.currentTime;
    if(nextPlayTime < now) nextPlayTime = now + 0.01; // small lead
    src.start(nextPlayTime);
    nextPlayTime += audioBuf.duration;
  } catch(e) {
    log('Playback error: '+ e,'error');
  }
}

function stopAllAssistantPlayback(){
  try{
    for(const s of assistantSources.slice()){
      try{ if(typeof s.stop === 'function') s.stop(0); } catch(_){}
      try{ s.disconnect(); } catch(_){}
    }
  }catch(e){ /* ignore */ }
  assistantSources = [];
  // reset scheduling so future audio plays immediately when resumed
  try{ nextPlayTime = audioContext.currentTime; } catch(_){}
  try{ log('stopAllAssistantPlayback executed at '+ new Date().toISOString(), 'debug'); } catch(_){}
}

// =============================
// SESSION MANAGEMENT
// =============================

async function startSession(){
  stopped = false;
  setSessionButtonState('starting');
  
  try {
    const response = await fetch('/start-session', {method:'POST'});
    const result = await response.json();
    
    if(!response.ok){
      handleStartSessionError(result, response.status);
      return;
    }
    
    // Session started successfully
    updateStatusUI(result.status || result);
    openEventSource();
    openAudioWebSocket();
    log('Session started successfully');
    
  } catch(error){
    handleStartSessionError(null, error.message);
  }
}

async function stopSession(){
  stopped = true;
  log('Stopping session…');
  
  // Stop server session
  try { await fetch('/stop-session', {method:'POST'}); } catch(_){ }
  
  // Clean up connections
  closeConnections();
  stopMicCapture();
  updateStatusUI({state:'stopped', message:'Session stopped.'});
}

function setSessionButtonState(state) {
  if(state === 'starting') {
    startBtn.disabled = true;
    stopBtn.disabled = false;
    startBtn.textContent = 'Starting…';
  } else if(state === 'stopped') {
    startBtn.disabled = false;
    stopBtn.disabled = true;
    startBtn.textContent = 'Start Session';
  }
}

function handleStartSessionError(result, errorInfo) {
  log('Failed to start: '+ (result?.status?.last_error || errorInfo), 'error');
  if(result) updateStatusUI(result.status || result);
  setSessionButtonState('stopped');
}

function closeConnections() {
  if(eventSource){ eventSource.close(); eventSource = null; }
  if(wsAudio){ wsAudio.close(); wsAudio = null; }
}

// =============================
// EVENT LISTENERS & INITIALIZATION
// =============================

startBtn.addEventListener('click', startSession);
stopBtn.addEventListener('click', stopSession);
window.addEventListener('beforeunload', closeConnections);

// Passive init (establish SSE early for existing session)
openEventSource();