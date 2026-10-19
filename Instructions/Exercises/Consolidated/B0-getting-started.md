---
lab:
    title: 'Getting started: set up your environment'
    description: 'Shared setup for the Build speech-enabled apps and agents lab: create a Microsoft Foundry project, deploy speech-capable models, get the starter code, and configure your environment. Complete this once before any task.'
    level: 300
    concepts: 'environment setup, Microsoft Foundry project, model deployment'
    status: 'draft'
---

# Getting started

This page sets up everything the **Build speech-enabled apps and agents** lab needs. **Every
task begins here** - complete this page first. Each task is written so you can then do it on
its own; if you're working through the whole lab in one sitting, you only need to do this
setup once.

**Your scenario:** you work at **Alpine Ski House**, a group of mountain resorts with lodges
in Zermatt, Whistler, and Chamonix. The guest services desk is buried in voicemail, and
guests call from all over the world in every language.

> **Note**: Some of the technologies used in this lab are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting, ensure you have:

- An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account) with permissions to provision Azure AI resources
- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Python version **3.13.xx**](https://www.python.org/downloads/release/python-31312/) installed\*
- [Git](https://git-scm.com/install/) installed and configured
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed
- A working microphone and speakers (a headset is strongly recommended for Tasks 3 and 5)

> \* Python 3.14 is available, but some dependencies are not yet compiled for that release. In particular, **pyaudio** (used by Task 5) has no wheel for Python 3.14. This lab has been tested with Python 3.13.12.

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used
to develop an AI solution. One project serves every task in this lab.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that open the first time you sign in, and if necessary use the Foundry logo at the top left to navigate to the home page.

1. If it is not already enabled, in the toolbar at the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name (for example, `alpine-voice-project`); expanding the **Advanced options** area to specify the following settings:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*\*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select **East US 2**\*\*

    > **TIP**: \* Remember (or make a note of) the Foundry resource name - you're going to need it for the endpoints below.

    > \*\* Speech-capable models are not available in every region. **East US 2** is the safest choice for Task 2. If you're only doing Tasks 1 and 3, any recommended Foundry region will do.

1. Select **Create** and wait for your project to be created. Then view its home page.

1. On the home page for your project, note that the API key, project endpoint, and OpenAI endpoint are displayed here.

    > **TIP**: You're going to need the project endpoint and the API key later - keep this tab open.

## Deploy speech-capable models

Task 2 uses generative AI models rather than the Speech service, so you need one model that
can *generate* speech and one that can *process* it. (Tasks 1 and 3 don't need these, so if
you're skipping Task 2 you can skip this section.)

### Deploy a text-to-speech model

1. Select **Explore models** (or on the **Discover** page, select the **Models** tab) to view the Microsoft Foundry model catalog.

1. In the model catalog, search for `gpt-4o-mini-tts`.

1. Review the model card, and then deploy the model using the default settings.

1. When the model has been deployed, view its details, noting that the **Target URI** and **Key** required to use it are available here. You'll need the Target URI.

    > **IMPORTANT**: `gpt-4o-mini-tts` is a recommended model for this exercise, not a required one. If it is unavailable in your region, deploy another supported text-to-speech model instead and use its name and Target URI throughout.

### Deploy a speech-to-text model

1. In the Foundry portal menu bar, select **Build**; and then view the **Deployments** page. Note that the text-to-speech model you deployed is listed.

1. Select **Deploy a base model**, and search the catalog for `gpt-4o-mini-transcribe`.

1. Deploy the model using the default settings.

1. Return to the **Deployments** page and verify that both models are listed. Select either one to view the **Target URI** you need for your code.

    > **IMPORTANT**: `gpt-4o-mini-transcribe` is a recommended model for this exercise, not a required one. If it is unavailable in your region, deploy another supported speech-to-text model instead.

## Get the starter code

1. Open Visual Studio Code.

1. Open the Command Palette (**Ctrl+Shift+P**), run **Git: Clone**, and enter:

    ```
    https://github.com/microsoftlearning/mslearn-ai-language.git
    ```

    You may be prompted to confirm you trust the authors.

1. Open the cloned repo, then **File > Open Folder** and select `mslearn-ai-language/Labfiles/B-build-speech-enabled-apps-and-agents/Python`. This single folder holds the starter code for **every** task in this lab - you use one virtual environment and one `.env` throughout.

1. In Visual Studio Code, view the **Extensions** pane; and if it is not already installed, install the **Python** extension.

1. Right-click **requirements.txt** and choose **Open in Integrated Terminal**. Then create a virtual environment and install packages:

    ```
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

    > **Note**: Opening the terminal this way in Visual Studio Code automatically activates the Python environment. You may need to enable running scripts on your system.

    > **Tip**: This installs everything for all five tasks in one go, including the Voice Live and audio packages used only by Task 5. If `pyaudio` fails to build, check that you're on Python 3.13 rather than 3.14.

## Configure your environment

The starter folder contains a **.env.example** file listing every setting this lab uses.

1. Copy **.env.example** to a new file named **.env** in the same folder.

1. Fill in the values for the tasks you plan to do:

    | Setting | Value | Used by |
    | --- | --- | --- |
    | `SPEECH_ENDPOINT` | The Azure AI services form of your resource endpoint: `https://{your-resource}.cognitiveservices.azure.com/` | Tasks 1, 3 |
    | `TTS_MODEL_ENDPOINT` | The **Target URI** of your text-to-speech model deployment | Task 2 |
    | `TTS_MODEL_NAME` | The deployment name, for example `gpt-4o-mini-tts` | Task 2 |
    | `STT_MODEL_ENDPOINT` | The **Target URI** of your speech-to-text model deployment | Task 2 |
    | `STT_MODEL_NAME` | The deployment name, for example `gpt-4o-mini-transcribe` | Task 2 |
    | `PROJECT_ENDPOINT` | The **full** project endpoint, including the `/api/projects/{project_name}` suffix | Task 4 |
    | `AGENT_NAME` | `slope-report-agent` (case-sensitive) | Task 4 |
    | `VOICELIVE_ENDPOINT` | The project endpoint with the `/api/projects/{project_name}` suffix **removed**: `https://{your-resource}.services.ai.azure.com/` | Task 5 |
    | `VOICELIVE_PROJECT_NAME` | The name of your Foundry project | Task 5 |
    | `VOICELIVE_AGENT_NAME` | `concierge-agent` (case-sensitive) | Task 5 |

    > **Important**: This lab uses three different endpoint formats, and mixing them up is
    > the most common cause of authentication errors. The **Speech tools** use
    > `cognitiveservices.azure.com`; **Voice Live** uses `services.ai.azure.com` with no
    > project suffix; **agent clients** use the full project endpoint *with* the suffix. The
    > **models** in Task 2 use their own per-deployment Target URIs, which are different again.

1. Save the **.env** file.

## Sign in to Azure

Every task in this lab authenticates with your Azure CLI sign-in.

1. In the terminal, sign in to Azure:

    ```powershell
    az login
    ```

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.

1. When prompted, follow the instructions to sign in. Then confirm the details of the subscription containing your Foundry resource.

## Check you're ready for a task

Each task needs specific values in your `.env`. Before starting a task, run the preflight
check from the `Labfiles/B-build-speech-enabled-apps-and-agents/Python` folder - the same
folder you opened in VS Code, where your terminal is already open. It reads your `.env` and
tells you what (if anything) is missing:

```
python ../setup/check_env.py --task 2
```

> **Tip**: The preflight check uses only the Python standard library, so it works even if
> you haven't run `pip install` yet or your `labenv` environment isn't activated. That
> makes it safe to run first when you jump straight into a task.

Swap `2` for the task number you're about to start. That's it - head to any task:

| Task | Page |
| --- | --- |
| Task 1 – Build the guest services line | [B1](B1-build-the-guest-services-line.md) |
| Task 2 – Use speech-capable AI models | [B2](B2-use-speech-capable-ai-models.md) |
| Task 3 – Translate spoken requests | [B3](B3-translate-spoken-requests.md) |
| Task 4 – Give an agent speech skills | [B4](B4-give-an-agent-speech-skills.md) |
| Task 5 – Build a real-time voice concierge | [B5](B5-build-a-real-time-voice-concierge.md) |
