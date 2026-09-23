# Lab A solution - Analyze and translate guest feedback

Complete, working reference implementations for every task in the **Analyze and translate
guest feedback** lab. Use these if you get stuck, or to check your own work.

Each file here is the finished version of the matching starter file in
`Labfiles/A-analyze-and-translate-text/Python/`.

> **Note on `check_env.py`**: the preflight check lives at the **lab root**
> (`Labfiles/A-analyze-and-translate-text/setup/check_env.py`) and is meant to be run from
> the **starter** `Python/` folder as `python ../setup/check_env.py --task N` - *not* from
> this `Solution/Python/` folder, where `../setup/` would resolve to a `Solution/setup/`
> folder that doesn't exist. The solution files below don't need it.

## File tree

```
Solution/Python/
  .env.example            Environment variables used by every task
  requirements.txt        Pinned package versions (same as the starter folder)
  analyze-reviews.py      Task 1 - detect language, extract entities, redact PII
  translate-feedback.py   Task 2 - translate guest feedback with Azure Translator
  review-agent.py         Task 3 - call the guest feedback agent from a client app
  reviews/                Sample Alpine Ski House guest reviews (review1-review5)
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
| Task 1 - Analyze guest reviews | `python analyze-reviews.py` | `FOUNDRY_ENDPOINT` |
| Task 2 - Translate guest feedback | `python translate-feedback.py` | `TRANSLATOR_ENDPOINT` |
| Task 3 - Guest feedback agent | `python review-agent.py` | `PROJECT_ENDPOINT`, `AGENT_NAME` |

Task 3 also needs the `guest-feedback-agent` agent to exist in your Foundry project, with
the Azure Language in Foundry Tools MCP server connected to it. You create that in the
portal as part of the task - it is not created by this code.

## Notes on the SDKs

- **Task 1** uses `azure-ai-textanalytics`, which talks to Azure Language in Foundry Tools
  directly. One call per document per capability, so the response is always a list; the
  code indexes `[0]` because each call sends a single document.
- **Task 2** uses `azure-ai-translation-text`. The `translate()` call detects the source
  language automatically when you don't pass `from_language`.
- **Task 3** uses `azure-ai-projects` to reach a portal agent by reference. The agent does
  the text analysis itself by calling the Azure Language MCP server, so the client app
  contains no text-analytics code at all - that contrast is the point of the task.

All three tasks authenticate with `DefaultAzureCredential`, so run `az login` first.
