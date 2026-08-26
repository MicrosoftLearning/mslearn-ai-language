---
lab:
    title: 'Task 3 – Translate spoken requests'
    description: 'Use Azure Speech in Foundry Tools to transcribe a spoken request and speak the translation back in three languages.'
    level: 300
    concepts: 'speech translation, multi-language targets, speech synthesis'
    islab: true
    status: 'draft'
---

# Task 3 — Translate spoken requests

*Part of the **Build speech-enabled apps and agents** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project, the starter code, and a working
> **microphone and speakers**. If you haven't already, complete [Getting
> started](B0-getting-started.md) to create your project, clone the code, and set
> `SPEECH_ENDPOINT` in `Python/.env`. You do **not** need any model deployments for this task.
> Then verify you're ready - run this from the `Python` folder, where your terminal is already
> open:

```
python ../setup/check_env.py --task 3
```

> **Continuing from a previous task?** If you completed Task 1, this task needs nothing new -
> it reuses the same `SPEECH_ENDPOINT` and the same virtual environment. If you came straight
> from Task 2, note that this task uses `SPEECH_ENDPOINT`, **not** the model Target URIs, so
> check that value is filled in before you start.

---

**Goal**: Let a guest speak a request at the front desk in English and have it appear - and
be spoken aloud - in French, Spanish, and Hindi.

**Concept reinforced**: translation recognition is a single operation that returns *many*
results. One pass over the microphone produces a dictionary of translations, one per target
language you registered.

**Set up:**

1. In the `Labfiles/B-build-speech-enabled-apps-and-agents/Python` folder, activate the
    virtual environment and confirm `SPEECH_ENDPOINT` is set in **.env**.

1. Open **translate-speech.py** and review the existing code.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, find the comment **Import namespaces** and add the code to
    import the namespaces you need:

    ```python
    # Import namespaces
    from azure.identity import DefaultAzureCredential
    import azure.cognitiveservices.speech as speech_sdk
    ```

## Configure translation

You need a *different* config class here. `SpeechTranslationConfig` extends the config you
used in Task 1 with the notion of target languages.

1. Find the comment **Configure translation** and add the following code to configure your
    connection and prepare to translate US English into French, Spanish, and Hindi:

    ```python
    # Configure translation
    credential = DefaultAzureCredential()
    translation_cfg = speech_sdk.translation.SpeechTranslationConfig(
        token_credential=credential,
        endpoint=speech_endpoint
    )
    translation_cfg.speech_recognition_language = 'en-US'
    translation_cfg.add_target_language('fr')
    translation_cfg.add_target_language('es')
    translation_cfg.add_target_language('hi')
    audio_in_cfg = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(
        translation_config=translation_cfg,
        audio_config=audio_in_cfg
    )
    print('Ready to translate from', translation_cfg.speech_recognition_language)
    ```

1. You use the **SpeechTranslationConfig** to translate speech into text, but you also need a
    plain **SpeechConfig** to synthesize the translations back into speech. Find the comment
    **Configure speech for synthesis of translations** and add:

    ```python
    # Configure speech for synthesis of translations
    speech_cfg = speech_sdk.SpeechConfig(
        token_credential=credential, endpoint=speech_endpoint)
    voices = {
        "fr": "fr-FR-HenriNeural",
        "es": "es-ES-ElviraNeural",
        "hi": "hi-IN-MadhurNeural"
    }
    print('Ready to use speech service.')
    ```

    Note that each target language needs a voice from *that* locale - you can't speak French
    text with an English voice and expect it to sound right.

## Translate the guest's speech

1. Find the comment **Translate guest speech** and add the following code:

    ```python
    # Translate guest speech
    print("Speak now...")
    translation_results = translator.recognize_once_async().get()
    print(f"Translating '{translation_results.text}'")
    ```

> **Try it first**: `translation_results.translations` is a dictionary keyed by the language
> codes you registered. For each one you need to print it *and* speak it - which means
> switching the synthesis voice between iterations. Write that loop before revealing the
> solution.

<details markdown="1">
<summary>Show a solution</summary>

Find the comment **Print and speak the translation results** and add the following code:

```python
# Print and speak the translation results
translations = translation_results.translations
for translation_language in translations:

    print(f"{translation_language}: '{translations[translation_language]}'")

    speech_cfg.speech_synthesis_voice_name = voices.get(translation_language)
    audio_out_cfg = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_cfg, audio_out_cfg)
    speak = speech_synthesizer.speak_text_async(translations[translation_language]).get()

    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
```

Save the changes to the code file, then run the application:

```
python translate-speech.py
```

When prompted, say something aloud - for example *"What time does the ski school open?"*

The program translates it into French, Spanish, and Hindi, then prints and speaks each
translation.

> **NOTE**: The translation to Hindi may not always be displayed correctly in the terminal
> due to character encoding issues. The spoken output is unaffected.

</details>

<details markdown="1" class="concept">
<summary>Why is this one call and not two?</summary>
<div class="concept-body" markdown="1">

You might expect to transcribe the audio, then send the text to a translation service - two
round trips. `TranslationRecognizer` does it in one, and that's not just a convenience.

Translating from a transcript loses information. The recognizer still has the acoustic
signal, so it can use prosody and hesitation to disambiguate - and because it knows the
target languages up front, it can produce all three translations from a single pass rather
than translating an already-lossy English string three times.

The trade-off is coupling: the source language is fixed at `en-US` here. If your guests
might speak *anything*, you'd add automatic source-language detection rather than assuming.

</div>
</details>

**Stretch**: the target languages are hard-coded. Add a fourth language of your choice, find
an appropriate voice for it in the
[voice catalogue](https://learn.microsoft.com/azure/ai-services/speech-service/language-support?tabs=tts),
and add it to both `add_target_language` and the `voices` dictionary.

---

**Next (optional):** [Task 4 — Give an agent speech skills](B4-give-an-agent-speech-skills.md)
