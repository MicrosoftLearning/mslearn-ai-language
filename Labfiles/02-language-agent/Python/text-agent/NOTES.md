# Notes: `text-agent.py`

**Exercise:** [Instructions/Exercises/02-language-agent.md](../../../../Instructions/Exercises/02-language-agent.md), *Develop a text analysis agent*

**Approach used in this lab:** **agent + MCP tool.** In the portal you create a Foundry agent, connect the **Azure Language MCP server** through a project connection, and set the tool's approval behaviour. The Python client then only **invokes the existing agent by name**.

**The other approach:** call the Language APIs **directly**, with `TextAnalyticsClient` or REST, as in [lab 01](../../../01-analyze-text/Python/text-analysis/NOTES.md).

> 🎯 marks an item that maps to the **AI-103** skills outline ([study guide, skills measured as of April 16, 2026](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)).

---

## 1. Project client: `AIProjectClient(endpoint=foundry_endpoint, credential=DefaultAzureCredential())`

| | |
|---|---|
| **Library** | `azure-ai-projects==2.0.0b4` (pinned; the API surface changed during preview) |
| **`endpoint`** | The **project** endpoint, `https://<resource>.services.ai.azure.com/api/projects/<project>`. |
| **`credential`** | Keyless Entra ID. The identity needs the **Foundry User** role (formerly *Azure AI User*) on the project. |
| **Why** | Entry point for everything in a project: agents, connections, deployments, evaluations, and the project-scoped OpenAI client. |
| **REST equivalent** | `Authorization: Bearer <token>` (scope `https://ai.azure.com/.default`) against `{project_endpoint}/...` |
| **Direct equivalent** | `TextAnalyticsClient(endpoint=<resource endpoint>, credential=...)` |

🎯 *Plan and manage → "**Configure an application to connect to a Foundry project**"*
🎯 *Manage, monitor, and secure → "…**keyless credentials**, and role policies"*

## 2. OpenAI client: `project_client.get_openai_client()`

| | |
|---|---|
| **Returns** | An `openai.OpenAI` client that is pre-authenticated and pointed at `{project_endpoint}/openai/v1`. |
| **Why** | Agents are invoked through the standard **Responses API**, so any OpenAI-compatible code can call them. |
| **Variant** | `get_openai_client(agent_name=...)` binds the agent, so `agent_reference` isn't needed on each call. |

## 3. Invoke the agent: `openai_client.responses.create(input=[...], extra_body={"agent_reference": {...}})`

```python
response = openai_client.responses.create(
    input=[{"role": "user", "content": prompt}],
    extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
)
print(response.output_text)
print(response.model_dump_json(indent=2))   # "View tool details"
```

| Parameter | Purpose |
|---|---|
| `input` | The user's message. Note that **there is no `model` and no `instructions`**: both come from the agent definition in the portal. |
| `extra_body.agent_reference` | Names the agent (and optionally a `version`) to run. `extra_body` is used because `agent_reference` is a Foundry extension, not part of the OpenAI schema. |
| Optional | `conversation=<id>` (from `openai_client.conversations.create()`) for multi-turn memory, and `stream=True` |
| Result | `output_text`, plus `output[]`, which contains **`mcp_list_tools`**, **`mcp_call`** (tool name, arguments and output) and `message` items. That's what the `model_dump_json` step shows. |

**Tool approval:** the exercise configures the Language tool's approval as *never*. If it were *always*, `response.output` would contain an `mcp_approval_request`, and the client would have to send an `mcp_approval_response` (`approve=True/False`, `approval_request_id=...`) in a follow-up `responses.create`.

| | |
|---|---|
| **REST equivalent** | `POST {project_endpoint}/openai/v1/responses` with body `{"input": [{"role": "user", "content": "..."}], "agent_reference": {"name": "Text-Analysis-Agent", "type": "agent_reference"}}` |
| **Direct equivalent** | The client picks the operation itself, for example `ai_client.recognize_pii_entities([text])`. There's no LLM in the loop: output is deterministic and costs no tokens, but the code has to know what's being asked. |

🎯 *Build agents → "Integrate agent tools, including APIs…"* and *"Define agent roles, goals, conversation-tracking approach, and **tool schemas**"*
🎯 *Responsible AI → "Govern agent behavior with oversight modes, constraints, and **tool-access controls**"* (the approval setting)
🎯 *Build agents → "Build autonomous or semiautonomous workflows with safeguards and **approval flow controls**"*
🎯 *Responsible AI → "Implement auditing through **trace logging**, provenance metadata…"*. `mcp_call` items show exactly which tool ran, with which arguments.
🎯 *Text analysis → "Configure detection of sentiment, tone… and sensitive content"* (through the tool)

---

## 4. Defining the same agent in code instead of the portal

```python
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

agent = project_client.agents.create_version(
    agent_name="Text-Analysis-Agent",
    definition=PromptAgentDefinition(
        model="gpt-4.1",
        instructions="Use the Azure Language tool to analyze text the user provides.",
        tools=[MCPTool(
            server_label="azure-language",
            server_url="https://<resource>.cognitiveservices.azure.com/language/mcp?api-version=2025-11-15-preview",
            project_connection_id="<language-connection>",   # holds the key header
            require_approval="never",
        )],
    ),
)
```

🎯 *Plan and manage → "Configure model and **agent deployments**"* · *"Integrate Foundry projects with **CI/CD** pipelines"*. Code-defined agents can be versioned and deployed from a pipeline.

## References

- [Azure Language tools and agents](https://learn.microsoft.com/azure/ai-services/language-service/concepts/foundry-tools-agents)
- [Connect agents to MCP servers](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)
- [AI-103 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)
