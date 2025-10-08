from __future__ import annotations

from pathlib import Path
import threading
import asyncio
import time
import logging
import traceback
from typing import Optional, Tuple, Union, cast, List, Dict, Any
import queue
import json
import base64
from aiohttp import web

from flask import Flask, render_template, jsonify, Response, request

app = Flask(__name__, 
           template_folder=str(Path(__file__).parent / "templates"),
           static_folder=str(Path(__file__).parent / "static"))

# ==============================================================================
# GLOBAL STATE & CONFIGURATION 
# ==============================================================================

# WebSocket server configuration
WS_SERVER_HOST = '0.0.0.0'
WS_SERVER_PORT = 8765

# Assistant state tracking
state_lock = threading.Lock()
assistant_state = {
    "state": "idle",
    "message": "Select 'Start Session' to begin a voice session.",
    "last_error": None,
    "connected": False,
}

# Threading components
assistant_thread: Optional[threading.Thread] = None
assistant_instance = None
assistant_loop: Optional[asyncio.AbstractEventLoop] = None
ws_server_thread: Optional[threading.Thread] = None

# Server-Sent Events client management
_sse_clients: List["queue.Queue[str]"] = []
_sse_clients_lock = threading.Lock()


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def _broadcast(event: Dict[str, Any]):
    """Broadcast SSE event to all connected clients."""
    data = f"data: {json.dumps(event)}\n\n"
    with _sse_clients_lock:
        # Remove dead clients while broadcasting
        dead_clients = []
        for client_queue in _sse_clients:
            try:
                client_queue.put_nowait(data)
            except Exception:
                dead_clients.append(client_queue)
        
        # Clean up disconnected clients
        for dead_client in dead_clients:
            _sse_clients.remove(dead_client)


# ==============================================================================
# WEBSOCKET AUDIO SERVER
# ==============================================================================

def _start_ws_server(host: str = WS_SERVER_HOST, port: int = WS_SERVER_PORT):
    """Start WebSocket server for low-latency binary audio streaming."""
    
    async def handle_audio_websocket(request):
        """Handle incoming WebSocket connections for binary audio data."""
        ws = web.WebSocketResponse(max_msg_size=10 * 1024 * 1024)
        await ws.prepare(request)
        
        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.BINARY and assistant_instance and assistant_loop:
                    # Convert binary PCM16 to base64 and send to assistant
                    audio_b64 = base64.b64encode(msg.data).decode('utf-8')
                    asyncio.run_coroutine_threadsafe(
                        assistant_instance.append_audio(audio_b64), 
                        assistant_loop
                    )
                elif msg.type == web.WSMsgType.ERROR:
                    break
        except Exception:
            pass  # Handle connection errors gracefully
        finally:
            await ws.close()
        
        return ws

    def run_websocket_server():
        """Run WebSocket server in dedicated thread."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def start_server():
            app = web.Application()
            app.router.add_get('/ws-audio', handle_audio_websocket)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host, port)
            await site.start()
            
            # Keep server running
            while True:
                await asyncio.sleep(3600)
        
        try:
            loop.run_until_complete(start_server())
        except Exception:
            pass

    # Start server in daemon thread
    thread = threading.Thread(target=run_websocket_server, daemon=True)
    thread.start()
    return thread


def set_state(state: str, message: str, *, error: str | None = None):
    """Update assistant state and broadcast to clients."""
    with state_lock:
        assistant_state["state"] = state
        assistant_state["message"] = message
        
        if error:
            assistant_state["last_error"] = error
            
        # Update connection status based on state
        if state in {"ready", "listening", "processing", "assistant_speaking"}:
            assistant_state["connected"] = True
        elif state in {"stopped", "idle"}:
            assistant_state["connected"] = False
    
    # Broadcast state change to all clients
    _broadcast({
        "type": "status",
        "state": state,
        "message": message,
        "last_error": assistant_state.get("last_error"),
        "connected": assistant_state.get("connected"),
    })


# Basic logging (can be overridden by parent app)
logger = logging.getLogger("real_time_voice.flask")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s in %(name)s: %(message)s")

# ---------------------------------------------------------------------------
# Suppress noisy 200 OK HTTP access logs (Werkzeug dev server) while keeping
# non-200 responses and internal status/log broadcasts. 
# ---------------------------------------------------------------------------
class _SuppressHTTP200(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401 - simple filter
        msg = record.getMessage()
        # Typical pattern: '127.0.0.1 - - [timestamp] "POST /audio-chunk HTTP/1.1" 200 -'
        # Suppress any line that clearly denotes an HTTP 200 access log.
        if '" 200 ' in msg:
            return False
        return True

werkzeug_logger = logging.getLogger("werkzeug")
# Avoid stacking multiple identical filters if code reloaded (Flask debug reload)
already = any(isinstance(f, _SuppressHTTP200) for f in getattr(werkzeug_logger, 'filters', []))
if not already:
    werkzeug_logger.addFilter(_SuppressHTTP200())


def _validate_env() -> Tuple[bool, str]:
    """Validate required environment variables."""
    import os
    
    required_vars = [
        "VOICE_LIVE_MODEL",
        "VOICE_LIVE_VOICE", 
        "AZURE_VOICE_LIVE_API_KEY",
        "AZURE_VOICE_LIVE_ENDPOINT"
    ]
    
    missing = [var for var in required_vars if not os.environ.get(var)]
    
    if missing:
        return False, f"Missing required environment variables: {', '.join(missing)}"
    
    return True, "Configuration valid"

class BasicVoiceAssistant:
    """Minimal assistant implementation for Voice Live API.
    
    Handles real-time voice conversation using Azure's Voice Live service.
    Manages connection, session configuration, and event processing.
    """

    # BEGIN VOICE LIVE ASSISTANT IMPLEMENTATION - ALIGN CODE WITH COMMENT


    
    # END VOICE LIVE ASSISTANT IMPLEMENTATION

        verbose_val = __import__('os').environ.get('VOICE_LIVE_VERBOSE', '0').strip()
        verbose = bool(int(verbose_val)) if verbose_val.isdigit() else False
        try:
            _broadcast({"type": "log", "level": "info", "msg": f"Connecting to Voice Live endpoint={self.endpoint} model={self.model} voice={self.voice}"})
            # Establish async connection to Azure Voice Live service with optimized settings
            async with connect(
                endpoint=self.endpoint,
                credential=self.credential,
                model=self.model,
                connection_options={"max_msg_size": 10 * 1024 * 1024, "heartbeat": 20, "timeout": 20},
            ) as conn:
                self.connection = conn
                # Reset cancellation flag at the start of a new connection/session
                self._response_cancelled = False

                # Configure voice: use AzureStandardVoice for locale-specific voices, plain string for others
                if self.voice.startswith("en-") or "-" in self.voice:
                    voice_cfg: Union[str, AzureStandardVoice] = AzureStandardVoice(name=self.voice)
                else:
                    voice_cfg = self.voice

                # BEGIN CONFIGURE VOICE LIVE SESSION - ALIGN CODE WITH COMMENT



                # END CONFIGURE VOICE LIVE SESSION

                # Main event processing loop - handle all Voice Live server events
                async for event in conn:
                    if self._stopping:
                        break
                    
                    await self._handle_event(event, conn, verbose)
        except Exception as e:
            tb = traceback.format_exc(limit=6)
            _broadcast({"type": "log", "level": "error", "msg": f"Connection failed: {e}", "trace": tb})
            self.state_callback("error", f"Connection failed: {e}")
            return

        # Cleanup (no local audio resources now)
        self.connection = None

    async def append_audio(self, audio_b64: str):
        """Send base64-encoded audio data to Voice Live input buffer."""
        if not self.connection:
            return
        try:
            await self.connection.input_audio_buffer.append(audio=audio_b64)
        except Exception as e:  # pragma: no cover
            logger.error("Failed to append audio: %s", e)

    # BEGIN HANDLE SESSION EVENTS - ALIGN CODE WITH COMMENT



    # END HANDLE SESSION EVENTS

def _run_assistant_bg():
    """Background thread target to run the async assistant until completion."""
    global assistant_instance, shutdown_requested, assistant_loop
    try:
        import os
        from azure.core.credentials import AzureKeyCredential, TokenCredential

        endpoint = os.environ.get("AZURE_VOICE_LIVE_ENDPOINT")
        model = os.environ.get("VOICE_LIVE_MODEL")
        voice = os.environ.get("VOICE_LIVE_VOICE")
        instructions = os.environ.get("VOICE_LIVE_INSTRUCTIONS") or "You are a helpful voice assistant."

        # Validate required environment variables using helper
        ok, msg = _validate_env()
        if not ok:
            set_state("error", msg)
            return

        # At this point _validate_env() ensured these are present; cast for type-checkers
        endpoint = cast(str, endpoint)
        model = cast(str, model)
        voice = cast(str, voice)

        # Use API key authentication for the web app (AZURE_VOICE_LIVE_API_KEY)
        api_key = os.environ.get("AZURE_VOICE_LIVE_API_KEY")
        if not api_key:
            set_state("error", "Missing AZURE_VOICE_LIVE_API_KEY environment variable")
            return
        credential = AzureKeyCredential(api_key)
        logger.info("Using API key authentication for Voice Live (AZURE_VOICE_LIVE_API_KEY)")

        def cb(state, message):
            set_state(state, message)

        assistant_instance = BasicVoiceAssistant(
            endpoint=endpoint,
            credential=credential,
            model=model,
            voice=voice,
            instructions=instructions,
            state_callback=cb,
        )
        assistant_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(assistant_loop)
        assistant_loop.run_until_complete(assistant_instance.start())
        set_state("stopped", "Session ended.")
    except Exception as e:  # pragma: no cover - runtime safety
        tb = traceback.format_exc(limit=6)
        logger.error("Assistant crashed: %s\n%s", e, tb)
        set_state("error", f"Assistant crashed: {e}", error=tb)
    finally:
        try:
            if assistant_loop and assistant_loop.is_running():
                assistant_loop.stop()
        except Exception:
            pass


@app.post("/start-session")
def start_session():
    global assistant_thread
    with state_lock:
        if assistant_state["state"] in {"starting", "ready", "listening", "processing", "assistant_speaking"}:
            return jsonify({"started": False, "status": assistant_state})

    ok, msg = _validate_env()
    if not ok:
        set_state("error", msg, error=msg)
        return jsonify({"started": False, "status": assistant_state}), 400

    with state_lock:
        assistant_state["state"] = "starting"
        assistant_state["message"] = "Starting voice session…"
        assistant_state["last_error"] = None
        assistant_state["connected"] = False

    assistant_thread = threading.Thread(target=_run_assistant_bg, daemon=True)
    assistant_thread.start()
    # Ensure websocket server for low-latency audio streaming is running
    global ws_server_thread
    if not ws_server_thread:
        try:
            ws_server_thread = _start_ws_server()
        except Exception:
            pass
    # Give the thread a brief moment to progress
    time.sleep(0.1)
    return jsonify({"started": True, "status": assistant_state})


@app.post("/stop-session")
def stop_session():
    global assistant_instance
    if not assistant_instance:
        return jsonify({"stopped": False, "reason": "No active session"}), 400
    assistant_instance.request_stop()
    set_state("stopped", "Stopping session…")
    return jsonify({"stopped": True})


@app.post("/interrupt")
def interrupt():
    """Request an interruption of the current assistant response.

    Attempt to cancel the active response on the assistant connection. If the
    SDK doesn't expose a cancel method, fall back to requesting a stop on the
    assistant instance.
    """
    global assistant_instance, assistant_loop
    if not assistant_instance or not assistant_loop:
        return jsonify({"interrupted": False, "reason": "No active session"}), 400
    try:
        # Mark response cancelled on the assistant instance immediately so the
        # event loop will suppress broadcasting further RESPONSE_AUDIO_DELTA events
        try:
            if assistant_instance:
                assistant_instance._response_cancelled = True
        except Exception:
            pass

        # Immediately instruct connected clients to stop any pending playback
        _broadcast({"type": "log", "level": "debug", "msg": f"Interrupt requested: broadcasting stop_playback at {time.time()}"})
        _broadcast({"type": "control", "action": "stop_playback"})

        # Also, stop assistant playback on the server-side audio processor (if present)
        try:
            ap = getattr(assistant_instance, 'connection', None)
            # The assistant_instance in this design doesn't own the audio processor when
            # running in the flask app variant; instead we attempt to stop playback via
            # any audio processor attached to assistant_instance (if available).
            ap_obj = getattr(assistant_instance, 'audio_processor', None)
            if ap_obj and hasattr(ap_obj, 'stop_playback') and assistant_loop:
                try:
                    # Schedule stop_playback to run promptly on the assistant loop
                    asyncio.run_coroutine_threadsafe(ap_obj.stop_playback(), assistant_loop)
                except Exception:
                    pass
        except Exception:
            pass

        # Schedule the SDK-level cancel immediately on the assistant loop for low latency
        try:
            conn = getattr(assistant_instance, "connection", None)
            resp = getattr(conn, "response", None) if conn else None
            if resp and hasattr(resp, "cancel") and assistant_loop:
                try:
                    asyncio.run_coroutine_threadsafe(resp.cancel(), assistant_loop)
                    _broadcast({"type": "log", "level": "info", "msg": "Interrupt scheduled (cancel)"})
                except Exception as e:
                    _broadcast({"type": "log", "level": "error", "msg": f"Failed to schedule cancel(): {e}"})
            else:
                _broadcast({"type": "log", "level": "warn", "msg": "No response.cancel() available; cannot perform graceful interrupt via SDK."})
        except Exception as e:
            _broadcast({"type": "log", "level": "error", "msg": f"Interrupt handler exception: {e}"})

        return jsonify({"interrupted": True})
    except Exception as e:
        return jsonify({"interrupted": False, "reason": str(e)}), 500


@app.post("/audio-chunk")
def audio_chunk():
    """Receive base64 PCM16 (24kHz mono) audio from browser."""
    global assistant_instance, assistant_loop
    if not assistant_instance or not assistant_loop:
        return jsonify({"accepted": False, "reason": "No active session"}), 400
    try:
        payload = request.get_json(silent=True) or {}
        audio_b64 = payload.get("audio")
        if not audio_b64:
            return jsonify({"accepted": False, "reason": "Missing audio field"}), 400
        # Schedule append inside assistant loop
        inst = assistant_instance
        if not inst:
            return jsonify({"accepted": False, "reason": "Assistant not ready"}), 503
        def _task():
            return asyncio.create_task(inst.append_audio(audio_b64))
        assistant_loop.call_soon_threadsafe(_task)
        return jsonify({"accepted": True})
    except Exception as e:  # pragma: no cover
        return jsonify({"accepted": False, "reason": str(e)}), 500


@app.get("/events")
def sse_events():
    """Server-Sent Events stream for status + audio."""
    q: "queue.Queue[str]" = queue.Queue()
    with _sse_clients_lock:
        _sse_clients.append(q)

    # Send current state immediately
    q.put_nowait(
        "data: "
        + json.dumps(
            {
                "type": "status",
                "state": assistant_state["state"],
                "message": assistant_state["message"],
                "last_error": assistant_state.get("last_error"),
                "connected": assistant_state.get("connected"),
            }
        )
        + "\n\n"
    )

    def gen():
        try:
            while True:
                msg = q.get()
                yield msg
        except GeneratorExit:  # client disconnected
            with _sse_clients_lock:
                if q in _sse_clients:
                    _sse_clients.remove(q)

    return Response(gen(), mimetype="text/event-stream")


@app.get("/status")
def status():
    with state_lock:
        return jsonify(assistant_state)


@app.get("/health")
def health():
    with state_lock:
        return jsonify({
            "ok": assistant_state.get("state") not in {"error"},
            "state": assistant_state.get("state"),
            "connected": assistant_state.get("connected"),
            "has_connection_obj": bool(assistant_instance and getattr(assistant_instance, 'connection', None)),
        }), 200


@app.get("/")
def index():
    """Render the main UI and expose selected environment variables for display.

    We intentionally show the *values* of a small set of environment variables
    so the developer or tester can confirm configuration in the browser.
    Values are displayed as the variable value or "(not set)" when missing.
    """
    import os

    env = {
        "VOICE_LIVE_MODEL": os.environ.get("VOICE_LIVE_MODEL") or "(not set)",
        "VOICE_LIVE_VOICE": os.environ.get("VOICE_LIVE_VOICE") or "(not set)",
        "AZURE_VOICE_LIVE_ENDPOINT": os.environ.get("AZURE_VOICE_LIVE_ENDPOINT") or "(not set)",
        "VOICE_LIVE_INSTRUCTIONS": os.environ.get("VOICE_LIVE_INSTRUCTIONS") or "(not set)",
    }
    return render_template("index.html", env=env)


# The root route is implemented above with environment values passed in.


def main() -> None:
    # Basic dev server; in production consider a WSGI/ASGI server like gunicorn or uvicorn.
    import os
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", "5000")))
    debug_env = os.environ.get("FLASK_DEBUG", os.environ.get("DEBUG", "0"))
    debug = bool(int(debug_env)) if str(debug_env).isdigit() else debug_env.lower() in ("1", "true", "yes")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":  # pragma: no cover
    main()
