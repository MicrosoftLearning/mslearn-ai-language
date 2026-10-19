---
lab:
    title: 'Task 3 – Hand the job to an agent'
    description: 'Connect the Azure Language in Foundry Tools MCP server to an agent so it can analyze text on request, then call that agent from your own client application.'
    level: 300
    concepts: 'agents, Model Context Protocol (MCP), tool approval, agent clients'
    islab: true
    status: 'draft'
---

# Task 3 — Hand the job to an agent

*Part of the **Analyze and translate guest feedback** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project, the starter code, and the **API
> key** and **project endpoint** from your project's home page in the Foundry portal. If you
> haven't already, complete [Getting started](A0-getting-started.md), then set
> `PROJECT_ENDPOINT` and `AGENT_NAME` in `Python/.env`. Note that `PROJECT_ENDPOINT` is the
> **full** endpoint including the `/api/projects/{project_name}` suffix - unlike the endpoint
> Task 1 used. Then verify you're ready - run this from the `Python` folder, where your
> terminal is already open:

```
python ../setup/check_env.py --task 3
```

> **Continuing from a previous task?** If you just finished an earlier task in the same
> `Python` folder, your project, virtual environment, and Azure sign-in are already set. You
> still need to add `PROJECT_ENDPOINT` and `AGENT_NAME` to your `.env`, and you need your
> project's **API key** to hand - then go straight to **Create an agent** below.

---

**Goal**: Give an agent the text-analysis capabilities you wrote by hand in Task 1, by
connecting the Azure Language in Foundry Tools MCP server - then call that agent from a
client app.

**Concept reinforced**: with an MCP server attached, the *agent* decides which operations to
call and in what order. Your client app shrinks to sending a prompt and printing a reply.

## Create an agent

1. In the [Microsoft Foundry portal](https://ai.azure.com), open your project and select
    **Create agents** (or on the **Build** page, select the **Agents** tab). Create a new
    agent named `guest-feedback-agent`.

    When ready, your agent opens in the agent playground.

1. In the model drop-down list, ensure that a current **gpt-5.1** (or later) chat model has
    been deployed and selected for your agent.

    > **Note**: Any current GA chat model works here. Model availability varies by region -
    > if `gpt-5.1` isn't offered in yours, select the newest available alternative.

1. Assign your agent the following **Instructions**:

    ```
    You are an AI agent that helps the Alpine Ski House guest experience team analyze guest reviews.
    ```

1. Use the **Save** button to save the changes.

1. Test the agent by entering the following prompt in the **Chat** pane:

    ```
    What can you help me with?
    ```

    The agent should respond with an appropriate answer based on its instructions. Note that
    right now it can only *talk* about analyzing reviews - it has no tools yet.

## Connect the Azure Language in Foundry Tools MCP server

Foundry includes an MCP server for Azure Language in Foundry Tools, which you can connect to
your project and use in your agent.

1. In the navigation pane on the left, select the **Tools** page.

1. Within the Tools page select the **Tools** tab.

1. Connect a tool; selecting **Azure Language in Foundry Tools** in the **Catalog** and
    connecting it to an endpoint, specifying the following configuration:
    - **Name**: *A unique name for your tool*
    - **Remote MCP Server endpoint**: `https://{foundry-resource-name}.cognitiveservices.azure.com/language/mcp?api-version=2025-11-15-preview`
    - **Parameters**: foundry-resource-name: *Your Foundry resource name*
    - **Authentication**: Key-based
    - **Ocp-Apim-Subscription-Key**: *API key for your Foundry project*

    > **Note**: If key-based authentication is disabled by a policy in your Azure
    > subscription, you can use Entra ID authentication to connect the agent to the Azure
    > Language service.

1. Wait for the MCP tool connection to be created, and then view its details page.

1. On the details page for the Azure Language in Foundry Tools connection, select **Use in
    an agent**, and then select the **guest-feedback-agent** agent you created previously.

    The agent should open in the playground, with the Azure Language tool connected.

    > **Note**: In some cases, the MCP tool is not added to the agent automatically. Verify
    > that **Azure Language in Foundry Tools** appears in the agent's tool list. If it does
    > not, add it manually from the available tools for the agent.

<details markdown="1" class="concept">
<summary>What is MCP actually doing here?</summary>
<div class="concept-body" markdown="1">

The Model Context Protocol is a standard way for a tool provider to *describe* what it can
do, so that any agent can discover and call it. When you connected that endpoint, the agent
fetched a list of available operations - things like `extract_named_entities_from_text` and
`detect_sentiment_from_text` - along with the parameters each one takes.

That's why you didn't have to write a schema for anything. In Task 1 you chose the operation
yourself; here the model reads the descriptions and picks. You'll see the exact tool names it
selected at the end of this task.

</div>
</details>

## Test the Azure Language tool in the playground

1. In the agent playground for the **guest-feedback-agent** agent, modify the instructions
    as follows:

    ```
    You are an AI agent that helps the Alpine Ski House guest experience team analyze guest reviews. Use the Azure Language tool to perform text analysis tasks.
    ```

1. Use the **Save** button to save the changes.

1. Test the agent by entering the following prompt in the **Chat** pane:

    ```
    Identify the PII entities in this review, and generate a redacted version:

    Superb lodge and outstanding staff. Alpine Ski House Zermatt, Switzerland. Spotless rooms, excellent service, and a fantastic location right below the Matterhorn. My colleague John Smith booked it for us and it was faultless. Contact me at alex@contoso.com for more details.
    ```

1. When prompted, approve use of the Azure Language tool by selecting **Always approve all
    Azure Language in Foundry Tools tools** (you may need to do this twice if the prompt asks
    for two distinct text analysis tasks).

    > **Note**: Depending on your environment, you may occasionally receive a 403, 502, or
    > other transient error after approving the tool. These errors are usually not blocking.
    > Refresh the page and retry the same prompt.

1. Review the response, which should identify the personally identifiable information in the
    review and create a redacted version - the same result you produced with code in Task 1.

1. Review the **Logs** for the chat and verify that the Azure Language tool was used by the
    agent to process the prompt.

## Configure tool approval

As you've seen in the playground, to use the tool the agent needs approval. Your client app
can't click an approval button, so configure the agent to approve automatically.

1. In the playground, in the list of **Tools** under the **Instructions**, in the menu for the
    Azure Language tool you added, select **Configure**.

1. Ensure that the **Approval setting for tools in this MCP server for this agent** setting is
    **Always auto-approve all tools** (if not, change it and add it).

1. Save any changes to the agent.

## Create a client application

Now that you have a working agent, you can create a client application that uses it.

1. In the `Labfiles/A-analyze-and-translate-text/Python` folder, open **review-agent.py** and
    review the existing code.

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

1. Find the comment **Get an OpenAI client** and add the code to get an OpenAI client with
    which to call your agent:

    ```python
    # Get an OpenAI client
    openai_client = project_client.get_openai_client()
    ```

> **Try it first**: The agent is called *by reference* - you send a prompt and name the
> agent, and the service resolves it. Look at the `extra_body` parameter and work out what
> shape it needs before revealing the solution.

<details markdown="1">
<summary>Show a solution</summary>

Find the comment **Use the agent to get a response** and add the code to submit a user
prompt to your agent and display the response:

```python
# Use the agent to get a response
prompt = input("User prompt: ")
response = openai_client.responses.create(
    input=[{"role": "user", "content": prompt}],
    extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
)

print(f"{agent_name}: {response.output_text}")
```

Save the file and run the application:

```powershell
python review-agent.py
```

When prompted, enter the following prompt:

```
Extract named entities from the following text: "Pierre and I stayed at Alpine Ski House Chamonix on July 14th."
```

Review the response, which should identify named people, places, and dates.

</details>

## View tool details

The Azure Language tool provides a wide range of functionality, and the agent must select the
appropriate function to call. You can see which ones it chose in the response.

1. In the **review-agent.py** code file, add the following line immediately after the
    `print(f"{agent_name}: {response.output_text}")` line you added previously (before the
    `except Exception as ex:` line):

    ```python
    print(f"\nResponse Details: {response.model_dump_json(indent=2)}")
    ```

1. Save the changes to the code file.

1. In the terminal, re-run the application (`python review-agent.py`).

1. When prompted, enter the following:

    ```
    Tell me what entities and dates are mentioned in this review, and whether it is positive or negative: "I booked our stay at Alpine Ski House Whistler in July, and it was fantastic!"
    ```

1. Review the response (you may need to scroll quite far up to see it), which should identify
    entities and dates, and determine the sentiment of the text.

1. Review the JSON response details, which indicate each of the tools available to the agent.
    In this case, it should have used the **extract_named_entities_from_text** and
    **detect_sentiment_from_text** tools within Azure Language in Foundry Tools.

    Notice what just happened: you asked for two different analyses in one sentence, and you
    wrote no code to route that request. Compare this file with **analyze-reviews.py** from
    Task 1 - the analysis logic didn't get simpler, it moved.

**Stretch**: your agent has the Language tool but not the Translator you used in Task 2. Add
a second prompt that asks the agent to summarize a review *and* translate the summary, and
see how it copes with a capability it wasn't given.

---

**Next:** You've completed the optional tasks. Head back to the [lab overview](A-analyze-and-translate-guest-feedback.md) for a summary and clean-up steps.
