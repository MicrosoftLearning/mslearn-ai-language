---
lab:
    title: 'Task 5 – Build a real-time voice concierge'
    description: 'Use Azure Speech Voice Live to build a real-time conversational voice agent, handling interruptions, echo cancellation, and background noise.'
    level: 400
    concepts: 'Voice Live, real-time audio, voice activity detection, barge-in, duplex conversation'
    islab: true
    status: 'draft'
---

# Task 5 — Build a real-time voice concierge

*Part of the **Build speech-enabled apps and agents** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project, the starter code, and a working
> **microphone and speakers** - ideally a headset. If you haven't already, complete
> [Getting started](B0-getting-started.md) to create your project, clone the code, and set
> `VOICELIVE_ENDPOINT`, `VOICELIVE_PROJECT_NAME`, and `VOICELIVE_AGENT_NAME` in `Python/.env`.
> You do **not** need any model deployments or a storage account for this task. Then verify
> you're ready:

```
python setup/check_env.py --task 5
```

> **Continuing from a previous task?** If you completed an earlier task in the same `Python`
> folder, your virtual environment and Azure sign-in are already set. This task uses a
> **third** endpoint format, though: `VOICELIVE_ENDPOINT` is the project endpoint with the
> `/api/projects/{project_name}` suffix **removed**, so it ends at the `.com` domain. Add
> that plus the project and agent names to your `.env`, then start at **Create an agent**.

> **TIP**: The application works best with a headset. With open speakers there's a risk the
> agent "hears" its own responses and processes them as new input - echo cancellation helps,
> but a headset removes the problem entirely.

---

**Goal**: Build a voice concierge that guests can genuinely converse with - one that listens
continuously, works out when they've finished speaking, and can be interrupted mid-sentence.

**Concept reinforced**: real-time voice is **event-driven**. You don't call "recognize" and
wait; you open a connection and react to a stream of events as the conversation unfolds.

## Create an agent

1. In the [Microsoft Foundry portal](https://ai.azure.com), open your project and select
    **Create agents** (or on the **Build** page, select the **Agents** tab). Create a new
    agent named `concierge-agent`.

    When ready, your agent opens in the agent playground.

1. In the model drop-down list, ensure that a current **gpt-5.1** (or later) chat model has
    been deployed and selected for your agent.

    > **Note**: Any current GA chat model works here. Model availability varies by region -
    > if `gpt-5.1` isn't offered in yours, select the newest available alternative.

1. Assign your agent the following **Instructions**:

    ```
    You are the Alpine Ski House voice concierge. You help guests with questions about the resort, the slopes, and their stay. You answer concisely and precisely, in a friendly tone suitable for being spoken aloud.
    ```

1. Use the **Save** button to save the changes.

1. Test the agent by entering the following prompt in the **Chat** pane:

    ```
    What can you help me with?
    ```

    The agent should respond with an appropriate answer based on its instructions.

## Configure Azure Speech Voice Live

Enabling voice mode for a Foundry agent integrates Azure Speech Voice Live, adding speech
capabilities to the agent.

1. In the pane on the left, under the model selection list, enable **Voice mode**.

    If the **Configuration** pane does not open automatically, use the "cog" icon above the
    chat interface to open it.

1. In the **Configuration** pane, under **Voice Live**, review the default speech input and
    output configuration. You can try different voices, previewing them until you decide
    which one suits a mountain resort concierge.

1. Close the **Configuration** pane and use the **Save** button to save the agent.

## Talk to the agent in the portal

Before writing any code, try the experience you're about to build.

1. In the Chat pane, use the **Start session** button to start a conversation with the agent.
    If prompted, allow access to the system microphone.

    The agent starts a speech session and listens for your prompt.

1. When the app status is **Listening...**, say something like *"What time do the lifts
    open?"* and wait for a response.

1. Verify that the app status changes to **Processing...**.

    > **Tip**: The processing speed may be so fast that you don't actually see the status before it changes to *Speaking*.

1. When the status changes to **Speaking...**, the app uses text-to-speech to vocalize the
    response. To see the original prompt and the response as text, select the **cc** button
    at the bottom of the chat screen.

    > **Tip**: The follow-on prompt is submitted just by speaking. You can even interrupt the agent to keep the interaction focused on what you need. You can also use the **Stop generation** button to stop long-running responses, but that button ends the conversation - you'll need to start a new one to continue.

1. To continue the conversation, just ask another question, such as *"Is there a ski school
    for beginners?"*, and review the response.

1. When you have finished, use the **X** icon to end the session. A transcript of the
    conversation is displayed.

## Implement the client application

To use your agent in a custom application, you need code that uses the Azure Speech Voice
Live SDK to initiate and manage a conversation session.

1. In the `Labfiles/B-build-speech-enabled-apps-and-agents/Python` folder, open
    **voice-concierge.py** and review the existing code.

    Most of the application scaffolding is provided. The **AudioProcessor** class (microphone
    and speaker handling) and the event handlers are already written - you implement the key
    steps that establish and run the conversation.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, find the comment **Import namespaces** and add the following:

    ```python
    # Import namespaces
    from azure.identity.aio import AzureCliCredential
    from azure.ai.voicelive.aio import connect
    from azure.ai.voicelive.models import (
        InputAudioFormat,
        Modality,
        OutputAudioFormat,
        RequestSession,
        ServerEventType,
        AudioNoiseReduction,
        AudioEchoCancellation,
        AzureSemanticVadMultilingual,
    )
    ```

    > **Note**: These are the **async** variants - `azure.identity.aio` and
    > `azure.ai.voicelive.aio`. A duplex conversation has to send and receive at the same
    > time, which is why this whole application is built on `asyncio`.

1. In the **main** function, note that code to load the configuration, create a credential,
    and construct and run a **VoiceConcierge** object has already been provided.

1. Under the **main** function, find the **VoiceConcierge** class definition. The `__init__`
    function is already implemented. You implement the **start** function, which is the core
    function that establishes the conversation session.

Work through the five steps in the `try` block of the **start** function. Each builds on the
previous one, and **steps 2 to 5 are nested inside the `async with` block from step 1**.

1. Find the comment **STEP 1: Connect Azure Speech Voice Live to the agent**, and add the
    following code (indenting it one level in under the `try:` statement):

    ```python
    # STEP 1: Connect Azure Speech Voice Live to the agent
    async with connect(
        endpoint=self.endpoint,
        credential=self.credential,
        api_version="2026-07-15",
        agent_name=self.agent_name,
        project_name=self.project_name,
    ) as connection:
        self.connection = connection
    ```

    This step opens a persistent connection to your agent so the Voice Live SDK can run a
    conversation with it.

1. Find the comment **STEP 2: Initialize audio processor**, and add the following code
    (indented *another level in*, under the step 1 code you just added):

    ```python
    # STEP 2: Initialize audio processor
    self.audio_processor = AudioProcessor(connection)
    ```

    This attaches an AudioProcessor, the utility class further down the file that manages
    audio hardware I/O.

1. Find the comment **STEP 3: Configure the session**, and add the following code (at the
    same indentation as the step 2 code):

    ```python
    # STEP 3: Configure the session
    await self.setup_session()
    ```

    This configures the session with the appropriate audio formats, conversational
    turn-detection semantics, and options to handle echo and background noise.

1. Find the comment **STEP 4: Start audio systems**, and add the following code (at the same
    indentation as the step 3 code):

    ```python
    # STEP 4: Start audio systems
    self.audio_processor.start_playback()

    print("\n[ready] Start speaking...")
    print("Press Ctrl+C to exit\n")
    ```

    This starts the audio processor so it plays back audio output. (Microphone capture starts
    a moment later, when the session-updated event arrives.)

1. Find the comment **STEP 5: Process events**, and add the following code (at the same
    indentation as the step 4 code):

    ```python
    # STEP 5: Process events
    await self.process_events()
    ```

    This runs the main loop that processes events such as speech input, response output, and
    interruptions.

1. Delete the `pass` placeholder line, then save the changes to the code file.

<details markdown="1">
<summary>Show a solution</summary>

The completed function should look like this:

```python
async def start(self):
    """Start the voice concierge."""
    print("\n" + "=" * 60)
    print(f"  ALPINE SKI HOUSE VOICE CONCIERGE - {self.agent_name}")
    print("=" * 60)

    # Add your code in this try block!
    try:
        # STEP 1: Connect Azure Speech Voice Live to the agent
        async with connect(
            endpoint=self.endpoint,
            credential=self.credential,
            api_version="2026-07-15",
            agent_name=self.agent_name,
            project_name=self.project_name,
        ) as connection:
            self.connection = connection

            # STEP 2: Initialize audio processor
            self.audio_processor = AudioProcessor(connection)

            # STEP 3: Configure the session
            await self.setup_session()

            # STEP 4: Start audio systems
            self.audio_processor.start_playback()

            print("\n[ready] Start speaking...")
            print("Press Ctrl+C to exit\n")

            # STEP 5: Process events
            await self.process_events()

    finally:
        if hasattr(self, 'audio_processor'):
            self.audio_processor.shutdown()
```

</details>

<details markdown="1" class="concept">
<summary>How does it know when I've stopped talking?</summary>
<div class="concept-body" markdown="1">

Look at `setup_session`, which is already written for you. The key line is
`turn_detection=AzureSemanticVadMultilingual()`.

Basic voice activity detection watches the audio level and calls a pause "the end". That's
why older phone systems cut you off mid-sentence when you paused to think. **Semantic** VAD
also considers whether what you've said so far sounds *finished* - so "the lifts open at..."
keeps listening, while "when do the lifts open?" doesn't.

The two lines below it matter just as much in a noisy resort lobby:
`AudioEchoCancellation()` stops the agent transcribing its own voice, and
`AudioNoiseReduction(type="azure_deep_noise_suppression")` filters out background chatter.
Between them they're the difference between a demo and something you'd put on a desk.

</div>
</details>

## Run the application

Now you're ready to run your application and have a conversation with your agent.

1. In the terminal, make sure you're signed in to Azure:

    ```powershell
    az login
    ```

    > **Note**: This task uses `AzureCliCredential` specifically, so an Azure CLI sign-in is required.

1. Run the client application:

    ```powershell
    python voice-concierge.py
    ```

1. When prompted, begin a conversation with the agent by asking a question such as *"What
    time does the ski school open?"*

1. Listen to the response and then continue the conversation. Try **interrupting** the agent
    mid-answer with a new question - the playback queue is cleared and it switches to your
    new question. That's the `INPUT_AUDIO_BUFFER_SPEECH_STARTED` event handler doing its job.

1. When you're finished, press **Ctrl+C** to end the conversation and stop the program.

**Stretch**: the event handlers print a plain-text trace of the conversation. Extend
`handle_event` to also append each guest utterance and agent reply to a transcript file, so
the front desk has a record of what was asked.

---

**Next:** You've completed the optional tasks. Head back to the [lab overview](B-build-speech-enabled-apps-and-agents.md) for a summary and clean-up steps.
