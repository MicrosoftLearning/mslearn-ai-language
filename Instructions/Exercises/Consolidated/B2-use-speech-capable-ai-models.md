---
lab:
    title: 'Task 2 – Use speech-capable AI models'
    description: 'Use generative AI models to generate and transcribe speech, steering delivery with natural-language instructions.'
    level: 300
    concepts: 'generative AI audio models, text-to-speech, speech-to-text, model endpoints'
    islab: true
    status: 'draft'
---

# Task 2 — Use speech-capable AI models

*Part of the **Build speech-enabled apps and agents** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project **plus two deployed models** -
> one text-to-speech and one speech-to-text. If you haven't already, complete
> [Getting started](B0-getting-started.md) to create your project, deploy both models, clone
> the code, and set `TTS_MODEL_ENDPOINT`, `TTS_MODEL_NAME`, `STT_MODEL_ENDPOINT`, and
> `STT_MODEL_NAME` in `Python/.env`. Then verify you're ready:

```
python setup/check_env.py --task 2
```

> **Continuing from a previous task?** If you just finished Task 1 in the same `Python`
> folder, your project, virtual environment, and Azure sign-in are already set. What Task 1
> did **not** need is the two model deployments - go back to
> [Getting started](B0-getting-started.md) and complete the *Deploy speech-capable models*
> section, then add the four model values to your `.env`. Note that these use each model's
> **Target URI**, not the `SPEECH_ENDPOINT` value Task 1 used.

---

**Goal**: Do the same two jobs as Task 1 - generate speech, transcribe speech - but with
generative AI models instead of the Speech service, and see what that changes.

**Concept reinforced**: speech-capable models take audio as just another modality. You talk
to them through the OpenAI SDK, and you can describe *how* something should be said in plain
language.

## Create a speech-generation app

1. In the `Labfiles/B-build-speech-enabled-apps-and-agents/Python` folder, open
    **generate-speech.py** and review the existing code.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, find the comment **Import namespaces** and add the code to
    import the namespaces you need to use the OpenAI SDK:

    ```python
    # Import namespaces
    from openai import AzureOpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    ```

1. In the **main** function, code to load the endpoint from the configuration file has
    already been provided. Find the comment **Create the Azure OpenAI client** and add the
    code to create a client:

    ```python
    # Create the Azure OpenAI client
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version="2025-03-01-preview"
    )
    ```

> **Try it first**: The speech call streams audio back rather than returning it in one
> piece, so it's used as a **context manager**. Look at the `speech_file_path` variable
> already defined above, and work out how the streamed response gets into it.

<details markdown="1">
<summary>Show a solution</summary>

Find the comment **Generate speech and save to file** and add the following code to submit a
prompt to the speech-generation model and save the response as a file:

```python
# Generate speech and save to file
with client.audio.speech.with_streaming_response.create(
    model=model_deployment,
    voice="alloy",
    input="Welcome to Alpine Ski House. The slopes open at eight.",
    instructions="Speak in a warm, welcoming tone.",
) as response:
    response.stream_to_file(speech_file_path)
```

Save the changes to the code file, then run the application:

```
python generate-speech.py
```

Observe the output as the code generates the requested speech and saves it in a file. The
code then plays the generated audio file.

Now change the `instructions` line to something quite different - for example
`Speak like an exhausted ski instructor at the end of a long season.` - and run it again.
Note that you changed *nothing* about the voice or the text, only the description of the
delivery.

</details>

<details markdown="1" class="concept">
<summary>Instructions versus SSML</summary>
<div class="concept-body" markdown="1">

In Task 1, controlling delivery meant picking a voice, and finer control means writing
**SSML** - an XML markup language where you annotate specific words with pitch, rate, and
emphasis. It's precise, deterministic, and tedious.

Here you described the delivery in a sentence. That's far quicker to iterate on, and it can
express things SSML struggles with ("sound apologetic but not grovelling"). The trade-off is
that it's non-deterministic - the same instruction can produce slightly different readings -
and you can't pin the emphasis on one exact syllable.

For a phone greeting recorded once, instructions are ideal. For a system that must say a
legal disclaimer identically every time, SSML still wins.

</div>
</details>

## Create a speech-transcription app

Now the other direction, using the speech-to-text model you deployed.

1. In the same folder, open **transcribe-speech.py** and review the existing code. Note that
    it reads `STT_MODEL_ENDPOINT` and `STT_MODEL_NAME`, and that it plays the sample
    **speech.wav** file before transcribing it.

1. At the top of the code file, find the comment **Import namespaces** and add the same
    imports you used above:

    ```python
    # Import namespaces
    from openai import AzureOpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    ```

1. Find the comment **Create the Azure OpenAI client** and add the same client code:

    ```python
    # Create the Azure OpenAI client
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version="2025-03-01-preview"
    )
    ```

    > **Note**: The client code is identical, but `endpoint` and `model_deployment` resolve
    > to your *transcription* model here. Each model deployment has its own Target URI.

> **Try it first**: Transcription is a single, non-streaming call. You open the audio file
> in binary mode and pass it through. What does `response_format="text"` change about what
> you get back?

<details markdown="1">
<summary>Show a solution</summary>

Find the comment **Call model to transcribe audio file** and add the following code:

```python
# Call model to transcribe audio file
audio_file = open(file_path, "rb")
transcription = client.audio.transcriptions.create(
    model=model_deployment,
    file=audio_file,
    response_format="text"
)

print(transcription)
```

Save the changes to the code file, then run the application:

```
python transcribe-speech.py
```

Observe the output as the code plays the audio file, submits it to the model for
transcription, and displays the result.

</details>

**Stretch**: `response_format` also accepts `"json"` and `"verbose_json"`. Switch to
`"verbose_json"` and print the whole object - you'll get segment timings and a detected
language, which is exactly what you'd need to build subtitles.

---

**Next (optional):** [Task 3 — Translate spoken requests](B3-translate-spoken-requests.md)
