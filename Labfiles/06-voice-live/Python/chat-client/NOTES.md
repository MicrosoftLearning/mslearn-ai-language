# Notes: `chat-client.py`

**Exercise:** [Instructions/Exercises/06-voice-live-agent.md](../../../../Instructions/Exercises/06-voice-live-agent.md), *Develop a Voice Live agent*

**Approach used in this lab:** **Voice Live** connects a microphone and speaker to an existing **Foundry agent** over a real-time **WebSocket**. The `azure-ai-voicelive` async SDK streams audio in both directions and raises server events (speech started, transcript, audio delta, and so on).

**The other approach:** build the voice loop yourself from **separate calls**: speech to text (lab 03 transcribe / lab 04 recognizer) → the agent through `responses.create` (labs 02/05) → text to speech (lab 03 generate / lab 04 synthesizer). An alternative is to call a **realtime model** directly (`gpt-realtime` through the OpenAI Realtime API) without an agent.

> 🎯 marks an item that maps to the **AI-103** skills outline ([study guide, skills measured as of April 16, 2026](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)).

> ⚠️ **Install note:** `requirements.txt` doesn't list the SDKs. The exercise installs them explicitly with `pip install -r requirements.txt azure-identity azure-ai-voicelive==1.2.0b4 --pre azure-ai-projects==2.0.0b4`. The pin matters: in newer `azure-ai-voicelive` releases, `connect()` takes `agent_name=` and `project_name=` instead of `agent_config=`.

---

## 1. Credential: `azure.identity.aio.AzureCliCredential()`

| | |
|---|---|
| **Why async** | `connect()` requires an **async** `TokenCredential`, so the credential comes from `azure.identity.aio`. |
| **Why CLI rather than Default** | Uses your `az login` session directly, which is predictable on a lab machine. In production, use `DefaultAzureCredential`, which supports managed identity. |
| **Alternative** | `AzureKeyCredential(key)` |

🎯 *Manage, monitor, and secure → "…**keyless credentials**…"*

## 2. Agent binding: `AgentConfig({"agent_name": ..., "project_name": ...})`

This tells Voice Live **which Foundry agent** answers. The agent's model, instructions and tools (including any MCP tools) are used unchanged. Voice Live adds only the speech layer.
🎯 *Speech → "**Integrate speech as an agent modality**…"*

## 3. Connect: `async with connect(endpoint, credential, api_version, agent_config) as connection:`

| Parameter | Purpose |
|---|---|
| `endpoint` | The Foundry resource endpoint, `https://<resource>.services.ai.azure.com/`. The SDK converts it to `wss://…/voice-live/realtime`. |
| `credential` | The async credential from §1. |
| `api_version` | `"2026-01-01-preview"` |
| `agent_config` | The agent and project from §2. |
| Returns | A `VoiceLiveConnection` WebSocket session. The `async with` block closes it cleanly. |

**REST/protocol equivalent:** there's no request/response REST call. It's a **WebSocket** (`wss://<resource>.services.ai.azure.com/voice-live/realtime?api-version=...`, plus agent and project query parameters) that exchanges JSON events with the same shape as the OpenAI Realtime protocol: client events such as `session.update` and `input_audio_buffer.append`, and server events such as `response.audio.delta`.

## 4. Configure the session: `connection.session.update(session=RequestSession(...))` (in `setup_session`)

| Setting | Purpose |
|---|---|
| `modalities=[TEXT, AUDIO]` | Return both a transcript and audio. |
| `input_audio_format` / `output_audio_format = PCM16` | 16-bit PCM at 24 kHz mono, matching the PyAudio settings. |
| `turn_detection=AzureSemanticVadMultilingual()` | **Semantic voice-activity detection**: the service decides when the user has *finished a thought* (not just paused), across many languages. |
| `input_audio_echo_cancellation=AudioEchoCancellation()` | Stops the agent hearing itself through the speakers. |
| `input_audio_noise_reduction=AudioNoiseReduction("azure_deep_noise_suppression")` | Server-side noise suppression. |
| Optional | `voice=AzureStandardVoice(name="en-US-Ava:DragonHDLatestNeural")` (or a custom voice), `instructions` (overrides), input transcription settings |

🎯 *Speech → "Integrate speech as an agent modality, including **custom speech models**"* (custom voices and speech models plug in here)
🎯 *Speech → "Enable **multimodal reasoning from audio inputs**"*

## 5. Audio in and out

| Call | Purpose |
|---|---|
| `connection.input_audio_buffer.append(audio=<base64 PCM>)` | Called from the PyAudio capture callback about every 50 ms. It runs `run_coroutine_threadsafe` because PyAudio's callbacks run on another thread. |
| `async for event in connection:` | Receives server events (in `process_events`). |
| `ServerEventType.RESPONSE_AUDIO_DELTA` → `event.delta` | Audio chunks, queued for playback. |
| `INPUT_AUDIO_BUFFER_SPEECH_STARTED` | The user started talking: **clear the playback queue**, so the user can interrupt (barge in). |
| `CONVERSATION_ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED` / `RESPONSE_AUDIO_TRANSCRIPT_DONE` | Text transcripts of the user and the agent, useful for logs and captions. |
| `ERROR` | `event.error.message` |

🎯 *Speech → "Implement workflows to convert speech to text and text to speech **for agentic interactions**"*
🎯 *Optimize → "Set up observability by implementing tracing, token analytics, safety signals, and **latency breakdowns**"*. Voice is latency-critical, and timestamps between `SPEECH_STOPPED` and the first `AUDIO_DELTA` are the key metric.

---

## 6. Voice Live vs a hand-built pipeline

| | Voice Live + agent (this lab) | STT → agent → TTS (labs 03–05) |
|---|---|---|
| Latency | Streaming end to end, with server VAD | Three sequential round trips |
| Interruptions | Built in (speech-started event) | You implement them |
| Noise and echo | Server-side DNS and AEC | You handle them |
| Control | Session settings | Full control of each stage (custom STT model, SSML, translation in between) |
| Agent tools/MCP | Inherited from the agent | Inherited from the agent |

🎯 *Plan and manage → "Choose the appropriate Foundry services for generative tasks… agent workflows, or **multimodal processing**"*

## References

- [Voice Live overview](https://learn.microsoft.com/azure/ai-services/speech-service/voice-live)
- [Voice Live with Foundry agents](https://learn.microsoft.com/azure/ai-services/speech-service/voice-live-agents-quickstart)
- [AI-103 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)
