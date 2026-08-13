---
lab:
    title: 'Task 1 – Build the guest services line'
    description: 'Use Azure Speech in Foundry Tools to synthesize a spoken greeting and transcribe recorded guest voicemail.'
    level: 200
    concepts: 'speech synthesis, speech recognition, neural voices'
    islab: true
    status: 'draft'
---

# Task 1 — Build the guest services line

*Part of the **Build speech-enabled apps and agents** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project and the starter code. If you
> haven't already, complete [Getting started](B0-getting-started.md) to create your project,
> clone the code, and set `SPEECH_ENDPOINT` in `Python/.env`. The sample voicemail recordings
> are already in the starter folder. You do **not** need to deploy any models for this task.
> Then verify you're ready - run this from the `Python` folder, where your terminal is already
> open:

```
python ../setup/check_env.py --task 1
```

---

**Goal**: Build the Alpine Ski House guest services line - an app that records a spoken
greeting for the phone system, and transcribes the voicemail guests leave.

**Concept reinforced**: one config, two directions. The same `SpeechConfig` drives both
synthesis and recognition; what changes is the **audio config** you attach to it - a file to
write, or a file to read.

**Set up:**

1. In the `Labfiles/B-build-speech-enabled-apps-and-agents/Python` folder, activate the
    virtual environment (`.\labenv\Scripts\Activate.ps1`) and confirm `SPEECH_ENDPOINT` is
    set in **.env** (see [Getting started](B0-getting-started.md)).

    > **Important**: `SPEECH_ENDPOINT` must be the Azure AI services form of your resource
    > endpoint - `https://{your-resource}.cognitiveservices.azure.com/`. The Foundry
    > resource name usually takes the form *{project_name}-resource*.

1. Open **guest-line.py** and review the existing code. The menu loop and the loop over the
    **messages** folder are already written; you'll add the speech handling.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

## Connect to Azure Speech in Foundry Tools

1. At the top of the code file, find the comment **Import namespaces** and add the code to
    import the namespaces you need:

    ```python
    # Import namespaces
    from azure.identity import DefaultAzureCredential
    import azure.cognitiveservices.speech as speech_sdk
    ```

1. In the **main** function, code to load the endpoint from the configuration file has
    already been provided. Find the comment **Create speech_config using Entra ID
    authentication** and add the code to create a Speech Configuration object:

    ```python
    # Create speech_config using Entra ID authentication
    credential = DefaultAzureCredential()
    speech_config = speech_sdk.SpeechConfig(
        token_credential=credential,
        endpoint=speech_endpoint)
    ```

1. Review the rest of the **main** function, and note that a loop has been implemented that
    enables the user to choose one of three options:
    1. Record a voice greeting
    1. Transcribe messages
    1. Exit the application

## Synthesize the greeting

The **record_greeting** function takes a line of text from the user and needs to turn it into
an audio file the phone system can play.

> **Try it first**: You need three things - somewhere to write the audio, a voice to speak
> in, and a synthesizer that combines them with the config. Which object provides "somewhere
> to write"? Sketch the code before revealing the solution.

<details markdown="1">
<summary>Show a solution</summary>

Find the **record_greeting** function, then find the comment **Synthesize the greeting
message to an audio file** and add the following code:

```python
output_file = "greeting.wav"
audio_config = speech_sdk.audio.AudioOutputConfig(filename=output_file)

speech_config.speech_synthesis_voice_name = "en-US-Serena:DragonHDLatestNeural"

speech_synthesizer = speech_sdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config
)

result = speech_synthesizer.speak_text_async(greeting_message).get()

if result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
    print(f"Greeting recorded and saved to {output_file}")
    speech_synthesizer = None  # Release the synthesizer resources
else:
    print("Error recording greeting: {}".format(result.reason))
```

Save the changes to the code file, then run the application:

```powershell
python guest-line.py
```

When prompted, enter **1** to record a greeting, then enter a greeting such as:

```
Thank you for calling Alpine Ski House. Our team is on the slopes right now. Please leave a message.
```

Wait while the speech is synthesized and saved as an audio file. You can select the
*greeting.wav* file that is generated in the folder to play it in Visual Studio Code.

</details>

<details markdown="1" class="concept">
<summary>Why does the voice name look like that?</summary>
<div class="concept-body" markdown="1">

`en-US-Serena:DragonHDLatestNeural` packs several things into one string: the **locale**
(`en-US`), the **voice persona** (`Serena`), and after the colon, the **model generation**
(`DragonHDLatestNeural`).

That last part matters. The Dragon HD voices are the current high-definition generation, and
using `Latest` means you automatically pick up improvements as they ship rather than pinning
to a snapshot. If you'd rather hear a different voice, browse the full catalogue in the
[language and voice support](https://learn.microsoft.com/azure/ai-services/speech-service/language-support?tabs=tts)
documentation - any voice name from that list drops straight into this line.

</div>
</details>

## Transcribe the voicemail

Now for the other direction. The **transcribe_messages** function already loops through the
`.wav` files in the **messages** folder and plays each one; you'll add the transcription.

> **Try it first**: This is the mirror image of what you just wrote. Swap the output audio
> config for an input one, swap the synthesizer for a recognizer, and check a different
> `ResultReason`. Try it before revealing the solution.

<details markdown="1">
<summary>Show a solution</summary>

In the **transcribe_messages** function, find the comment **Transcribe the audio file** and
add the following code:

```python
# Transcribe the audio file
audio_config = speech_sdk.audio.AudioConfig(filename=file_path)
speech_recognizer = speech_sdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=audio_config
)
result = speech_recognizer.recognize_once_async().get()
if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
    print(f"Transcription: {result.text}")
else:
    print("Error transcribing message: {}".format(result.reason))
```

Save the changes to the code file, then run the application again:

```powershell
python guest-line.py
```

When prompted, enter **2** to transcribe messages. View the transcription for each message -
each file is played back automatically, so you can hear the message and check the
transcription against it.

</details>

**Stretch**: `recognize_once_async` stops at the first pause, so it only handles short
utterances. Look up **continuous recognition** in the Speech SDK and adapt
`transcribe_messages` so it can handle a long, rambling voicemail without truncating it.

---

**Next:** [Task 2 — Use speech-capable AI models](B2-use-speech-capable-ai-models.md)
