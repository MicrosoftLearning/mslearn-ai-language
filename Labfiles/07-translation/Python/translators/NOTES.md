# Notes: `translate-text.py` and `translate-speech.py`

**Exercise:** [Instructions/Exercises/07-translation.md](../../../../Instructions/Exercises/07-translation.md), *Translate text and speech*

**Approach used in this lab:** call **Azure Translator in Foundry Tools** directly with `azure-ai-translation-text` for text, and **Azure Speech translation** (Speech SDK) to recognize English speech, translate it into French, Spanish and Hindi, and speak each translation.

**The other approach:**
- **LLM-powered translation:** an agent or model translates through its instructions (`responses.create(instructions="Translate to French", input=text)`). It gives better control of tone and terminology, but output isn't deterministic.
- **An agent with a translation tool:** wrap Translator as a function or OpenAPI tool, or an MCP server, so the agent chooses when to translate and the result is deterministic.
- **Spoken agents:** Voice Live (lab 06) with multilingual VAD, plus agent instructions to reply in the user's language.

> 🎯 marks an item that maps to the **AI-103** skills outline ([study guide, skills measured as of April 16, 2026](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)).

---

# Part A: `translate-text.py`

## A1. Client: `TextTranslationClient(credential=DefaultAzureCredential(), endpoint=foundry_endpoint)`

| | |
|---|---|
| **Library** | `azure-ai-translation-text==1.0.1` |
| **`endpoint`** | The Foundry resource endpoint, `https://<resource>.cognitiveservices.azure.com/`. A custom-domain endpoint is required for Entra ID auth. |
| **`credential`** | Keyless Entra ID. The identity needs *Cognitive Services User*. The key alternative is `AzureKeyCredential(key)` plus `region=`. |
| **REST equivalent** | `Authorization: Bearer <token>` (scope `https://cognitiveservices.azure.com/.default`) on `{endpoint}/translator/text/v3.0/...` |

🎯 *Manage, monitor, and secure → "…**keyless credentials**…"*

## A2. Supported languages: `client.get_supported_languages(scope="translation")`

| | |
|---|---|
| **Returns** | `.translation`, a dict of language code → name/dir. The code validates the user's choice against its keys. Other scopes are `transliteration` and `dictionary`. |
| **REST equivalent** | `GET {endpoint}/translator/text/v3.0/languages?api-version=3.0&scope=translation` (no auth required on the global endpoint) |

## A3. Translate: `client.translate(body=[InputTextItem(text=...)], to_language=[target])`

| Parameter | Purpose |
|---|---|
| `body` | A list of `InputTextItem` (or plain strings). Up to 1,000 elements per request. |
| `to_language` | **A list**: one call can translate into several languages at once. |
| Optional | `from_language` (skip auto-detection), `text_type="html"`, `profanity_action="Marked"` (with `profanity_marker`), `category=<custom translator id>`, `include_alignment`, `include_sentence_length` |
| Result | A list of `TranslatedTextItem`: `.detected_language.language` (with `.score`) and `.translations[]` (`.to`, `.text`) |

| | |
|---|---|
| **Why** | Fast and deterministic neural MT, with **automatic source-language detection**, profanity handling and **Custom Translator** domain models. |
| **REST equivalent** | `POST {endpoint}/translator/text/v3.0/translate?api-version=3.0&to=fr` with body `[{"Text": "..."}]` |
| **LLM equivalent** | `responses.create(model=..., instructions=f"Translate the user's text into {target}. Return only the translation.", input=text)` |

🎯 *Text analysis → "Build solutions that **translate text by using Azure Translator in Foundry Tools or LLM-powered translation flows**"*
🎯 *Text analysis → "Configure detection of… safety issues, and sensitive content"* (`profanity_action`)
🎯 *Text analysis → "Customize language model outputs for domain tasks…"* (Custom Translator `category`, or LLM instructions)

---

# Part B: `translate-speech.py`

## B1. Translation config: `speech_sdk.translation.SpeechTranslationConfig(token_credential, endpoint)`

| Setting | Purpose |
|---|---|
| `token_credential=DefaultAzureCredential()` | Keyless Entra ID |
| `endpoint` | The Foundry resource endpoint |
| `speech_recognition_language = 'en-US'` | The **source** spoken language. Auto-detection is possible with `AutoDetectSourceLanguageConfig`. |
| `add_target_language('fr' / 'es' / 'hi')` | Target **text** languages. They're all produced from one recognition pass. |

## B2. Recognizer: `TranslationRecognizer(translation_config, audio_config=AudioConfig(use_default_microphone=True))`

`recognize_once_async().get()` listens for one utterance and returns a `TranslationRecognitionResult`:
- `.text` is the recognized English text.
- `.translations` is a dict `{"fr": "...", "es": "...", "hi": "..."}`.

For long sessions, use `start_continuous_recognition_async()` with `recognizing`/`recognized` events, which also give live partial translations.

## B3. Speak each translation: `SpeechConfig(...)` + `SpeechSynthesizer(speech_cfg, AudioOutputConfig(use_default_speaker=True))`

| | |
|---|---|
| **Why a second config** | `SpeechTranslationConfig` produces *text* translations. A separate `SpeechConfig` with a per-language **neural voice** (`fr-FR-HenriNeural`, `es-ES-ElviraNeural`, `hi-IN-MadhurNeural`) speaks them. |
| **`speak_text_async(text).get()`** | Synthesizes to the speaker. Check `ResultReason.SynthesizingAudioCompleted`. |
| **Alternative** | `translation_cfg.voice_name = "..."` with a `synthesizing` event handler gives built-in audio output for a **single** target language. |

| | |
|---|---|
| **REST equivalent** | There's no single REST call for live speech translation; it's a WebSocket protocol, which is why the Speech SDK is used. For files, transcribe with fast/batch transcription, then call Translator `translate`, then TTS REST. |
| **Agent equivalent** | Voice Live (lab 06) connected to an agent instructed to "Reply in the language the user speaks", or STT → agent (LLM translation) → TTS. |

🎯 *Speech → "**Translate speech into other languages** by using language models and Foundry Tools"*
🎯 *Speech → "Implement workflows to convert speech to text and text to speech…"*
🎯 *Plan and manage → "Choose an appropriate model for each task, including LLMs… and **Foundry Tools**"*. Translator/Speech (deterministic, custom glossaries) versus LLM translation (tone and context) is that choice.

## References

- [Translator text SDK](https://learn.microsoft.com/azure/ai-services/translator/text-translation/sdk-overview)
- [Speech translation](https://learn.microsoft.com/azure/ai-services/speech-service/speech-translation)
- [AI-103 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)
