# Lab B solution - Build speech-enabled apps and agents

Complete, working reference implementations for every task in the **Build speech-enabled
apps and agents** lab. Use these if you get stuck, or to check your own work.

Each file here is the finished version of the matching starter file in
`Labfiles/B-build-speech-enabled-apps-and-agents/Python/`.

## File tree

```
Solution/Python/
  .env.example              Environment variables used by every task
  requirements.txt          Pinned package versions (same as the starter folder)
  guest-line.py             Task 1 - synthesize a greeting, transcribe guest voicemail
  generate-speech.py        Task 2 - text-to-speech with a generative AI model
  transcribe-speech.py      Task 2 - speech-to-text with a generative AI model
  translate-speech.py       Task 3 - translate spoken guest requests in real time
  speech-agent-client.py    Task 4 - call the speech agent from a client app
  voice-concierge.py        Task 5 - real-time voice conversation with Voice Live
  messages/                 Sample guest voicemail recordings (message_1, message_2)
  speech.wav                Sample audio used by transcribe-speech.py
```

## How to run each task

From the `Solution/Python` folder, create a virtual environment, install the packages,
and copy `.env.example` to `.env` with your own values:

```
python -m venv labenv
.\labenv\Scripts\Activate.ps1
pip install -r requirements.txt
az login
```

| Task | Command | Needs in `.env` |
| --- | --- | --- |
| Task 1 - Guest services line | `python guest-line.py` | `SPEECH_ENDPOINT` |
| Task 2 - Generative AI speech | `python generate-speech.py` then `python transcribe-speech.py` | `TTS_MODEL_ENDPOINT`, `TTS_MODEL_NAME`, `STT_MODEL_ENDPOINT`, `STT_MODEL_NAME` |
| Task 3 - Translate speech | `python translate-speech.py` | `SPEECH_ENDPOINT` |
| Task 4 - Speech agent client | `python speech-agent-client.py` | `PROJECT_ENDPOINT`, `AGENT_NAME` |
| Task 5 - Voice concierge | `python voice-concierge.py` | `VOICELIVE_ENDPOINT`, `VOICELIVE_PROJECT_NAME`, `VOICELIVE_AGENT_NAME` |

Tasks 4 and 5 also need agents that you create in the Foundry portal as part of those
tasks - they are not created by this code. Task 4 needs `slope-report-agent` with the
Azure Speech in Foundry Tools MCP server connected; Task 5 needs `concierge-agent` with
voice mode enabled.

## Notes on the SDKs

- **Tasks 1 and 3** use `azure-cognitiveservices-speech`, the Azure Speech SDK. Both build
  a config object from your Foundry endpoint plus a `DefaultAzureCredential`, then attach
  an audio config that points at a file, the microphone, or the speaker.
- **Task 2** uses the `openai` SDK against model deployments rather than the Speech
  service. The same Foundry resource serves both, but the endpoints differ: Task 2 uses
  each model's **Target URI**, not the Azure AI services endpoint.
- **Task 4** uses `azure-ai-projects` to reach a portal agent by reference. The agent
  performs the speech work by calling the Azure Speech MCP server, so this client app
  contains no Speech SDK code at all.
- **Task 5** uses `azure-ai-voicelive`. Note that `connect()` takes `agent_name` and
  `project_name` as separate keyword arguments, and the `pyaudio` dependency has no wheel
  for Python 3.14 - use Python 3.13 for this lab.

Tasks 1-4 authenticate with `DefaultAzureCredential` and Task 5 with `AzureCliCredential`,
so run `az login` first either way.
