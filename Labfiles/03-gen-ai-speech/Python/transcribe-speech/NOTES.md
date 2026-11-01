# Notes: `transcribe-speech.py`

**Exercise:** [Instructions/Exercises/03-gen-ai-speech.md](../../../../Instructions/Exercises/03-gen-ai-speech.md), *Use speech-capable generative AI models* (speech-transcription section)

**Approach used in this lab:** call a **generative speech-to-text model** (`gpt-4o-mini-transcribe`) directly through the OpenAI SDK's `AzureOpenAI` client.

**The other approach:** an **agent** hears the user through **Voice Live** (lab 06), or calls the **Azure Speech MCP server**'s speech-to-text tool on an audio file in blob storage (lab 05).

> 🎯 marks an item that maps to the **AI-103** skills outline ([study guide, skills measured as of April 16, 2026](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)).

---

## 1. Client

`AzureOpenAI(azure_endpoint=..., azure_ad_token_provider=token_provider, api_version="2025-03-01-preview")` is identical to the one in [generate-speech/NOTES.md](../generate-speech/NOTES.md) §1, and uses keyless Entra ID auth.
🎯 *"…**keyless credentials**…"* · *"Configure an application to connect to a Foundry project"*

## 2. Transcribe: `client.audio.transcriptions.create(model, file, response_format)`

```python
with open(file_path, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model=model_deployment, file=audio_file, response_format="text")
print(transcription)
```

| Parameter | Purpose |
|---|---|
| `model` | STT deployment name (`gpt-4o-mini-transcribe`, `gpt-4o-transcribe` or `whisper`). |
| `file` | An open binary file (wav, mp3, m4a, webm…). The upload is sent as multipart form data. The code opens it in a `with` block so the handle is closed. The exercise uses a bare `open()`. |
| `response_format` | `"text"` returns a plain string, which is why `print(transcription)` works. `"json"` returns an object with `.text`. Whisper also supports `"verbose_json"`, `"srt"` and `"vtt"` with timestamps. |
| Optional | `language="en"` (improves accuracy and latency), `prompt="Contoso, Fabrikam"` (vocabulary and spelling hints), `temperature`, `stream=True` (incremental transcript events) |

| | |
|---|---|
| **REST equivalent** | `POST {endpoint}/openai/deployments/{deployment}/audio/transcriptions?api-version=2025-03-01-preview`, multipart, with `file=@speech.wav`, `model=...` and `response_format=text` |
| **Classic Azure Speech equivalent** | `speech_sdk.SpeechRecognizer(...).recognize_once_async()` (lab 04) for short audio, continuous recognition for streams, or the **fast transcription** / batch REST APIs for files. These add speaker diarization, custom speech models and phrase lists. |
| **Agent equivalent** | **Voice Live** (lab 06) transcribes live microphone input for an agent. With the **Speech MCP** tool (lab 05), the agent gets a SAS URL to an audio file and calls `recognize`. |

🎯 *Speech → "Implement workflows to convert **speech to text** and text to speech for agentic interactions"*
🎯 *Speech → "Enable **multimodal reasoning from audio inputs**"*. A transcript is the bridge that lets an LLM reason over speech. Audio-native models do it directly.
🎯 *Plan and manage → "Choose an appropriate model for each task…"*. Generative STT (simple, robust, prompt hints) versus Azure Speech STT (custom models, diarization, real-time streaming) is that choice.

## References

- [Azure OpenAI speech to text (Whisper / gpt-4o-transcribe)](https://learn.microsoft.com/azure/foundry/openai/whisper-quickstart)
- [Connect Azure Speech to an agent (MCP)](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/azure-ai-speech)
- [AI-103 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)
