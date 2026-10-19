---
lab:
    title: 'Task 4 – Give an agent speech skills'
    description: 'Connect the Azure Speech in Foundry Tools MCP server to an agent so it can synthesize and transcribe speech on request, then call that agent from a client application.'
    level: 300
    concepts: 'agents, Model Context Protocol (MCP), tool approval, blob storage, SAS tokens'
    islab: true
    status: 'draft'
---

# Task 4 — Give an agent speech skills

*Part of the **Build speech-enabled apps and agents** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project, the starter code, your project's
> **API key**, and an **Azure storage account** that you create below. If you haven't already,
> complete [Getting started](B0-getting-started.md), then set `PROJECT_ENDPOINT` and
> `AGENT_NAME` in `Python/.env`. Note that `PROJECT_ENDPOINT` is the **full** endpoint
> including the `/api/projects/{project_name}` suffix. You do **not** need any model
> deployments or a microphone for this task. Then verify you're ready - run this from the
> `Python` folder, where your terminal is already open:

```
python ../setup/check_env.py --task 4
```

> **Continuing from a previous task?** If you completed an earlier task in the same `Python`
> folder, your project, virtual environment, and Azure sign-in are already set. This task
> needs two genuinely new things that no earlier task did: an **Azure storage account with a
> SAS token**, and `PROJECT_ENDPOINT` / `AGENT_NAME` in your `.env`. Start at **Create an
> Azure storage account** below.

---

**Goal**: Give an agent the speech capabilities you wrote by hand in Task 1, by connecting
the Azure Speech in Foundry Tools MCP server - then call that agent from a client app.

**Concept reinforced**: the agent needs somewhere to *put* the audio it generates. Unlike
your code, which wrote `greeting.wav` next to the script, a hosted agent writes to blob
storage and hands you back a URL.

## Create an Azure storage account

The Azure Speech MCP server uses an Azure storage account to save the audio files it
generates.

1. Open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`, and sign in using your Azure credentials.

1. Create a new **Azure storage account** resource with the following settings:
    - **Subscription**: *Your subscription*
    - **Resource group**: *Use the same resource group as your Foundry resource*
    - **Storage account name**: *A unique name for your storage account*
    - **Region**: *Any available region*
    - **Preferred storage type**: Azure blob storage or Azure Data Lake Storage Gen2
    - **Primary workload**: Cloud native
    - **Performance**: Standard
    - **Redundancy**: Locally-redundant storage (LRS)

1. When the Azure storage account resource has been created, go to it in the portal.

1. In the left navigation pane for the storage account, expand **Data storage**, and select **Containers**.

1. Add a new container named **files**. This is where your agent will save the audio files it generates.

1. In the context menu (**...**) for the **files** container, select **Generate SAS**, and create a SAS token with the following details:
    - **Signing method**: Account key
    - **Signing key**: Key1
    - **Stored access policy**: None
    - **Permissions**:
        - Read
        - Add
        - Create
        - Write
        - List
    - **Start and expiry date/time**:
        - **Start**: The current date and time
        - **Expiry**: 11:59pm tomorrow
    - **Allowed IP addresses**: *Leave blank*
    - **Allowed protocols**: HTTPS only

    > **IMPORTANT**: Copy the generated SAS token and URL, and store them in a text file for now - you'll need them in a moment, and the portal won't show them to you again.

## Create an agent

1. In the [Microsoft Foundry portal](https://ai.azure.com), open your project and select
    **Create agents** (or on the **Build** page, select the **Agents** tab). Create a new
    agent named `slope-report-agent`.

    When ready, your agent opens in the agent playground.

1. In the model drop-down list, ensure that a current **gpt-5.1** (or later) chat model has
    been deployed and selected for your agent.

    > **Note**: Any current GA chat model works here. Model availability varies by region -
    > if `gpt-5.1` isn't offered in yours, select the newest available alternative.

1. Assign your agent the following **Instructions**:

    ```
    You are an AI agent for Alpine Ski House that uses the Azure Speech tool to transcribe and generate speech.
    ```

1. Use the **Save** button to save the changes.

1. Test the agent by entering the following prompt in the **Chat** pane:

    ```
    What can you help me with?
    ```

    The agent should respond with an appropriate answer based on its instructions.

## Create an Azure Speech in Foundry Tools connection

1. In the navigation pane on the left, select the **Tools** page.

1. On the **Tools** tab, connect a tool; selecting **Azure Speech MCP Server** in the
    **Catalog** and connecting it to an endpoint, specifying the following configuration:
    - **Name**: *A unique name for your tool*
    - **Remote MCP Server endpoint**: `https://{foundry-resource-name}.cognitiveservices.azure.com/speech/mcp?api-version=2025-11-15-preview`
    - **Parameters**: foundry-resource-name: *Your Foundry resource name*
    - **Authentication**: Key-based
    - **Ocp-Apim-Subscription-Key**: *API key for your Foundry project*
    - **X-Blob-Container-Url**: *The SAS URL for your storage container*

    > **Note**: If key-based authentication is disabled by a policy in your Azure
    > subscription, you can use Entra ID authentication to connect the agent to the Azure
    > Speech service.

1. Wait for the MCP tool connection to be created, and then view its details page.

1. On the details page for the Azure Speech in Foundry Tools connection, select **Use in an
    agent**, and then select the **slope-report-agent** agent you created previously.

    The agent should open in the playground, with the Azure Speech tool connected.

    > **Note**: In some cases, the MCP tool is not added to the agent automatically. Verify
    > that the Azure Speech tool appears in the agent's tool list. If it does not, add it
    > manually from the available tools for the agent.

## Test the Azure Speech tool in the playground

1. In the agent playground for the **slope-report-agent** agent, enter the following prompt:

    ```
    Generate "Fresh powder on all upper runs. Lifts open at eight." as speech
    ```

1. When prompted, approve use of the Azure Speech tool by selecting **Always approve all
    Azure Speech MCP Server tools**.

1. Review the response, which should include a link to the generated audio file. Then select
    the link to hear the synthesized speech.

    That link points into the blob container you created - which is why the agent needed a
    storage account and your Task 1 code did not.

1. Enter the following prompt:

    ```
    Transcribe the file at https://microsoftlearning.github.io/mslearn-ai-language/Labfiles/05-speech-tool/speech_1.wav
    ```

1. If prompted, approve use of the Azure Speech tool.

    > **Note**: If a transient error occurs while calling the tool, refresh the page and retry the same prompt.

1. Review the output, which should be a transcription of the audio file.

## Configure tool approval

Your client app can't click an approval button, so configure the agent to approve
automatically before you call it from code.

1. In the playground, in the list of **Tools** under the **Instructions**, in the menu for the
    Azure Speech tool you added, select **Configure**.

1. Ensure that the **Approval setting for tools in this MCP server for this agent** setting is
    **Always auto-approve all tools** (if not, change it and add it).

1. Save any changes to the agent.

## Create a client application

1. In the `Labfiles/B-build-speech-enabled-apps-and-agents/Python` folder, open
    **speech-agent-client.py** and review the existing code. Note that it already contains a
    loop that reads prompts until you enter `quit`.

1. At the top of the code file, find the comment **Import namespaces** and add the following:

    ```python
    # Import namespaces
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    ```

1. In the **main** function, find the comment **Get project client** and add the code to
    create a client for your Foundry project:

    ```python
    # Get project client
    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(),
    )
    ```

1. Find the comment **Get an OpenAI client** and add:

    ```python
    # Get an OpenAI client
    openai_client = project_client.get_openai_client()
    ```

> **Try it first**: The agent is called *by reference* - you send a prompt and name the
> agent, and the service resolves it. Notice that this client contains **no Speech SDK code
> at all**. Write the call before revealing the solution.

<details markdown="1">
<summary>Show a solution</summary>

Find the comment **Use the agent to get a response** and add the code to submit the prompt
and display the response:

```python
# Use the agent to get a response
response = openai_client.responses.create(
    input=[{"role": "user", "content": prompt}],
    extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
)

print(f"{agent_name}: {response.output_text}")
```

Save the changes and run the application:

```powershell
python speech-agent-client.py
```

When prompted, enter the following prompt:

```
Synthesize "Better a witty fool, than a foolish wit!" as speech using the voice "en-GB-SoniaNeural".
```

Review the response, which should include a clickable link to a generated audio file.

After checking out the generated audio file, enter the following prompt:

```
Transcribe https://microsoftlearning.github.io/mslearn-ai-language/Labfiles/05-speech-tool/speech_2.wav
```

Review the response. To exit the program, enter `quit` (or just press Enter).

</details>

<details markdown="1" class="concept">
<summary>Where did the audio plumbing go?</summary>
<div class="concept-body" markdown="1">

Compare this file with **guest-line.py** from Task 1. There you created a config, an audio
config, a synthesizer, called `speak_text_async`, and checked a `ResultReason`. Here you
sent a sentence.

The work didn't vanish - it moved behind the MCP server, which is running the same Speech
service you called directly. What you traded away is control: you can't stream the audio,
you can't write it to a specific local path, and you depend on blob storage and a SAS token
that expires.

That's the honest trade. An agent is excellent when requests are open-ended and varied. For
a nightly batch job transcribing a voicemail box, Task 1's code is simpler, cheaper, and has
fewer moving parts.

</div>
</details>

**Stretch**: ask the agent to do something it needs *two* tool calls for, such as
"Transcribe that file and then read the transcript back to me in a French voice." Then add
`print(f"\nResponse Details: {response.model_dump_json(indent=2)}")` after the print
statement to see which tools it chose.

---

**Next (optional):** [Task 5 — Build a real-time voice concierge](B5-build-a-real-time-voice-concierge.md)
