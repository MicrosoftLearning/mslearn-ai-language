# Notes: `voice-mail.py`

**Exercise:** [Instructions/Exercises/04-azure-speech.md](../../../../Instructions/Exercises/04-azure-speech.md), *Recognize and synthesize speech*

**Approach used in this lab:** call **Azure Speech in Foundry Tools** directly with the **Speech SDK** (`azure-cognitiveservices-speech`): neural text to speech to record a greeting, and speech recognition to transcribe voicemail WAV files.

**The other approach:** a **Foundry agent** with the **Azure Speech MCP server** tool, which does the same speech-to-text and text-to-speech on files in blob storage. That's what lab [05-speech-tool](../../../05-speech-tool/Python/speech-client/NOTES.md) builds.

> 🎯 marks an item that maps to the **AI-103** skills outline ([study guide, skills measured as of April 16, 2026](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)).

---

## 1. Config: `speech_sdk.SpeechConfig(token_credential=credential, endpoint=foundry_endpoint)`

| | |
|---|---|
| **`token_credential`** | `DefaultAzureCredential()`, giving **Entra ID (keyless)** auth. The SDK fetches and refreshes tokens itself. Older code used `subscription=key, region=...`, and `FOUNDRY_KEY` in `.env` is an unused leftover of that. |
| **`endpoint`** | The Foundry resource endpoint, `https://<resource>.cognitiveservices.azure.com/`. |
| **Why** | One config object carries auth, endpoint, voice and recognition language, and is shared by synthesizers and recognizers. |
| **RBAC** | The identity needs *Cognitive Services Speech User* or *Cognitive Services User* on the resource. |

🎯 *Manage, monitor, and secure → "…managed identity… **keyless credentials**, and role policies"*

## 2. Synthesize: `SpeechSynthesizer(speech_config, audio_config).speak_text_async(text).get()`

| | |
|---|---|
| **`AudioOutputConfig(filename="greeting.wav")`** | Writes the audio to a file. `use_default_speaker=True` plays it instead. |
| **`speech_synthesis_voice_name`** | `"en-US-Serena:DragonHDLatestNeural"`, a **Dragon HD** neural voice. Any voice from the voice gallery works, including a **custom neural voice** endpoint. |
| **`speak_text_async(text).get()`** | Starts synthesis and blocks for the result. `speak_ssml_async(ssml)` gives control over prosody, pauses, pronunciation and multiple voices. |
| **Result check** | `result.reason == ResultReason.SynthesizingAudioCompleted`. Otherwise inspect `result.cancellation_details`. |
| **REST equivalent** | `POST https://<region>.tts.speech.microsoft.com/cognitiveservices/v1` with an SSML body, headers `Content-Type: application/ssml+xml` and `X-Microsoft-OutputFormat: riff-24khz-16bit-mono-pcm`, and a bearer token or key |
| **Agent/MCP equivalent** | The Speech MCP tool's **text-to-speech** operation. Prompt the agent with something like "Synthesize speech with voice en-US-JennyNeural from text …", and the WAV is written to blob storage through a container SAS URL. |

🎯 *Speech → "Implement workflows to convert speech to text and **text to speech** for agentic interactions"*
🎯 *Speech → "Integrate speech as an agent modality, including **custom speech models**"* (custom neural voices plug into `speech_synthesis_voice_name`)

## 3. Recognize: `SpeechRecognizer(speech_config, AudioConfig(filename=...)).recognize_once_async().get()`

| | |
|---|---|
| **`AudioConfig(filename=file_path)`** | Reads a WAV file. `use_default_microphone=True` listens live instead. |
| **`recognize_once_async()`** | Recognizes a **single utterance**, up to about 15 seconds or the first long pause, which is fine for short voicemails. For longer audio, use `start_continuous_recognition_async()` with `recognized` event handlers, or batch/fast transcription. |
| **Optional** | `speech_config.speech_recognition_language = "en-GB"`, `PhraseListGrammar` (domain vocabulary), a custom speech `endpoint_id` |
| **Result check** | `result.reason == ResultReason.RecognizedSpeech` → `result.text`. `NoMatch` means no recognizable speech, and `Canceled` means an error (see `cancellation_details`). |
| **REST equivalent** | Fast transcription: `POST {endpoint}/speechtotext/transcriptions:transcribe?api-version=2024-11-15`, multipart, with `audio=@file.wav` and `definition={"locales":["en-US"]}`. Or the short-audio REST endpoint for clips under 60 seconds. |
| **Agent/MCP equivalent** | The Speech MCP tool's **speech-to-text** operation on a blob **SAS URL**: "Recognize this English audio file located in <SAS URL>". |

🎯 *Speech → "Implement workflows to convert **speech to text**…"*

---

## 4. Direct Speech SDK vs agent + Speech MCP

| | Direct Speech SDK (this lab) | Agent + Speech MCP (lab 05) |
|---|---|---|
| Audio I/O | Local files, microphone and speaker | Files in **Azure Blob Storage** through SAS URLs |
| Control | Full: voices, SSML, phrase lists, continuous recognition | What the tool exposes, driven by natural-language prompts |
| Composition | You write the logic (record, then transcribe) | The LLM chains steps, such as "transcribe this and summarize it" |
| Secrets | Entra ID in the app | Speech key in a **project connection**; SAS URLs must be short-lived and narrowly scoped |

🎯 *Plan and manage → "Choose appropriate memory, tool, and knowledge integration services for agent solutions"*

## References

- [Speech SDK overview](https://learn.microsoft.com/azure/ai-services/speech-service/speech-sdk)
- [Connect Azure Speech to an agent (MCP)](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/azure-ai-speech)
- [AI-103 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)
