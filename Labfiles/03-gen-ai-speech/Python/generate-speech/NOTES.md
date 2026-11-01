# Notes: `generate-speech.py`

**Exercise:** [Instructions/Exercises/03-gen-ai-speech.md](../../../../Instructions/Exercises/03-gen-ai-speech.md), *Use speech-capable generative AI models* (speech-generation section)

**Approach used in this lab:** call a **generative text-to-speech model** (`gpt-4o-mini-tts`) directly through the OpenAI SDK's **`AzureOpenAI`** client, and stream the audio to an MP3.

**The other approach:** let an **agent** speak, through **Voice Live** (lab 06, real-time speech in and out for a Foundry agent) or through the **Azure Speech MCP server** tool (lab 05), which synthesizes audio to blob storage.

> 🎯 marks an item that maps to the **AI-103** skills outline ([study guide, skills measured as of April 16, 2026](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)).

---

## 1. Client: `AzureOpenAI(azure_endpoint, azure_ad_token_provider, api_version)`

```python
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
client = AzureOpenAI(azure_endpoint=endpoint, azure_ad_token_provider=token_provider,
                     api_version="2025-03-01-preview")
```

| | |
|---|---|
| **Class** | `openai.AzureOpenAI`, the Azure-flavoured client that builds `/openai/deployments/{deployment}/...?api-version=...` URLs. |
| **`azure_endpoint`** | `https://<resource>.openai.azure.com/` (resource root, **without** `/openai/v1`) |
| **`azure_ad_token_provider`** | A callable that returns Entra ID tokens and refreshes them automatically, so the code is **keyless**. |
| **`api_version`** | Required for this client. The audio APIs here use a preview version. |
| **Why `AzureOpenAI` here, when the other labs use `OpenAI`?** | Audio endpoints were first exposed on the versioned (deployment-based) API. With the v1 API you could equally use `OpenAI(base_url="https://<resource>.openai.azure.com/openai/v1/", api_key=token_provider)`. |

🎯 *Manage, monitor, and secure → "…**keyless credentials**, and role policies"* · *"Configure an application to connect to a Foundry project"*

## 2. Generate speech: `client.audio.speech.with_streaming_response.create(...)`

```python
with client.audio.speech.with_streaming_response.create(
        model=model_deployment, voice="alloy",
        input="My voice is my passport!", instructions="Speak in a serious tone.") as response:
    response.stream_to_file(speech_file_path)
```

| Parameter | Purpose |
|---|---|
| `model` | TTS deployment name (`gpt-4o-mini-tts`). |
| `voice` | A preset voice: `alloy`, `ash`, `coral`, `echo`, `nova`, `sage`, `shimmer`, and others. |
| `input` | The text to speak. |
| `instructions` | **Style steering**: tone, emotion, pacing or accent, given in natural language. This is what makes it *generative* TTS. Classic neural TTS uses SSML instead (see lab 04). |
| Optional | `response_format` (`mp3` by default, or `wav`, `opus`, `aac`, `flac`, `pcm`) and `speed` |
| `with_streaming_response` | Streams the bytes to disk as they arrive instead of buffering the whole file in memory. `stream_to_file()` writes the MP3. |

| | |
|---|---|
| **REST equivalent** | `POST {endpoint}/openai/deployments/{deployment}/audio/speech?api-version=2025-03-01-preview` with body `{"model": "...", "input": "...", "voice": "alloy", "instructions": "..."}`. The response is binary audio. |
| **Classic Azure Speech equivalent** | `speech_sdk.SpeechSynthesizer(...).speak_text_async(text)` with a neural voice (lab 04), or `speak_ssml_async` for fine control. |
| **Agent equivalent** | **Voice Live** with an agent (lab 06) for real-time spoken replies, or the **Speech MCP** text-to-speech tool (lab 05), which saves a WAV to blob storage and returns a link. |

🎯 *Speech → "Implement workflows to convert speech to text and **text to speech** for agentic interactions"*
🎯 *Plan and manage → "Choose an appropriate model for each task…"*. Generative TTS (style through `instructions`) versus neural TTS (SSML, custom voice) is that choice.
🎯 *Optimize → "Tune generation behavior, such as prompt engineering…"*. `instructions` is prompt engineering for voice.

## 3. `playsound(speech_file_path)`

This plays the MP3 locally through the `playsound3` package. It doesn't call any AI service.

## References

- [Azure OpenAI audio (text to speech)](https://learn.microsoft.com/azure/foundry/openai/text-to-speech-quickstart)
- [Connect Azure Speech to an agent (MCP)](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/azure-ai-speech)
- [AI-103 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)
