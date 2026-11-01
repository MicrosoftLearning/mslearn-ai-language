# Notes: `speech-client.py`

**Exercise:** [Instructions/Exercises/05-azure-speech-mcp.md](../../../../Instructions/Exercises/05-azure-speech-mcp.md), *Use Azure Speech in an agent*

**Approach used in this lab:** **agent + MCP tool.** In the portal you create a Foundry agent, add the **Azure Speech MCP server** through a connection (Speech key plus a blob container SAS URL for output audio), and test it in the playground. The Python client loops, sending each prompt to the agent by name.

**The other approach:** call the **Speech SDK directly**, as in [lab 04 voice-mail](../../../04-azure-speech/Python/voice-mail/NOTES.md), or use the generative audio models (lab 03).

> 🎯 marks an item that maps to the **AI-103** skills outline ([study guide, skills measured as of April 16, 2026](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)).

---

## 1. Calls in this file

| Call | Purpose | Details |
|---|---|---|
| `AIProjectClient(endpoint=foundry_endpoint, credential=DefaultAzureCredential())` | Connect to the **project** (`.../api/projects/<project>`) with keyless auth | Same as [lab 02 NOTES](../../../02-language-agent/Python/text-agent/NOTES.md) §1 |
| `project_client.get_openai_client()` | An OpenAI-compatible client scoped to the project | §2 there |
| `openai_client.responses.create(input=[{"role": "user", "content": prompt}], extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}})` | Run the `speech-agent`. Its model, instructions and Speech MCP tool are all defined server-side. | §3 there |

🎯 *"Configure an application to connect to a Foundry project"* · *"…**keyless credentials**…"*

**REST equivalent** of each turn: `POST {project_endpoint}/openai/v1/responses` with body `{"input": [...], "agent_reference": {"name": "speech-agent", "type": "agent_reference"}}`.

## 2. What happens server-side on a prompt like "Transcribe <SAS URL>"

1. The agent's model sees the Speech MCP tool's schema (`mcp_list_tools`) and decides to call speech-to-text.
2. Foundry calls the **remote Speech MCP server**, authenticating with the **project connection** (the Speech key never reaches the client).
3. The MCP server fetches the audio from the **SAS URL**, transcribes it, and returns text (an `mcp_call` output item).
4. The model writes the final answer (`output_text`). For text to speech, the server writes a WAV to your container and returns a link.

🎯 *Build agents → "Integrate agent tools, including APIs, knowledge stores, search, content understanding, and custom functions"*
🎯 *Speech → "**Integrate speech as an agent modality**…"*
🎯 *Speech → "Implement workflows to convert speech to text and text to speech **for agentic interactions**"*

## 3. Conversation state: a gap in this client

Each loop iteration sends a **new, stateless** request: there's no `conversation` and no `previous_response_id`. So "now summarize that transcript" won't remember the previous turn. To fix it:

```python
conversation = openai_client.conversations.create()          # before the loop
response = openai_client.responses.create(conversation=conversation.id, input=[...],
                                          extra_body={"agent_reference": {...}})
```

🎯 *Build agents → "Define agent roles, goals, **conversation-tracking approach**, and tool schemas"*
🎯 *Build agents → "Build agents that integrate retrieval, function-calling, and **conversation memory**"*

## 4. Security considerations (from the tool docs)

- **SAS URLs are secrets.** Use the shortest practical expiry and the narrowest scope (a single blob or container), and don't paste them into transcripts that get logged.
- The Speech MCP tool **doesn't support network-secured (private) Foundry**.
- The agent needs a **tool-calling** model.

🎯 *Manage, monitor, and secure → "Configure security, including… **private networking**…"*
🎯 *Responsible AI → "Govern agent behavior with… **tool-access controls**"*

## 5. The same agent in code, and the direct alternative

```python
# Agent definition (instead of the portal)
from azure.ai.projects.models import PromptAgentDefinition, MCPTool
project_client.agents.create_version(agent_name="speech-agent", definition=PromptAgentDefinition(
    model="gpt-4.1", instructions="Use the Speech tool to transcribe or synthesize audio.",
    tools=[MCPTool(server_label="azure-speech", server_url=SPEECH_MCP_URL,
                   project_connection_id=SPEECH_CONNECTION, require_approval="never")]))

# Direct alternative (no agent): see lab 04
speech_sdk.SpeechRecognizer(speech_config, speech_sdk.audio.AudioConfig(filename="msg.wav")).recognize_once_async().get()
```

## References

- [Connect Azure Speech in Foundry Tools to an agent](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/azure-ai-speech)
- [Connect agents to MCP servers](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)
- [AI-103 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)
