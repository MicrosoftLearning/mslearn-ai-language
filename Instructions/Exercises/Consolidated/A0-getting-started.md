---
lab:
    title: 'Getting started: set up your environment'
    description: 'Shared setup for the Analyze and translate guest feedback lab: create a Microsoft Foundry project, get the starter code, and configure your environment. Complete this once before any task.'
    level: 300
    concepts: 'environment setup, Microsoft Foundry project'
    status: 'draft'
---

# Getting started

This page sets up everything the **Analyze and translate guest feedback** lab needs. **Every
task begins here** - complete this page first. Each task is written so you can then do it on
its own; if you're working through the whole lab in one sitting, you only need to do this
setup once.

**Your scenario:** you work at **Alpine Ski House**, a group of mountain resorts with lodges
in Zermatt, Whistler, and Chamonix. Guests leave reviews in a dozen languages, and the guest
experience team needs to publish the useful ones without publishing anyone's email address.

> **Note**: Some of the technologies used in this lab are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting, ensure you have:

- An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account) with permissions to provision Azure AI resources
- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Python version **3.13.xx**](https://www.python.org/downloads/release/python-31312/) installed\*
- [Git](https://git-scm.com/install/) installed and configured
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed
- Basic familiarity with Python

> \* Python 3.14 is available, but some dependencies are not yet compiled for that release. This lab has been tested with Python 3.13.12.

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used
to develop an AI solution. One project serves every task in this lab.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that open the first time you sign in, and if necessary use the Foundry logo at the top left to navigate to the home page.

1. If it is not already enabled, in the toolbar at the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name (for example, `alpine-feedback-project`); expanding the **Advanced options** area to specify the following settings:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*\*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select any available region

    > **Note**: Use a recommended Microsoft Foundry region. Model availability may vary by region.

    > **TIP**: \* Remember (or make a note of) the Foundry resource name - you're going to need it for the endpoints below.

1. Select **Create** and wait for your project to be created. Then view its home page.

1. On the home page for your project, note that the API key, project endpoint, and OpenAI endpoint are displayed here.

    > **TIP**: You're going to need the project endpoint and the API key later - keep this tab open.

## Get the starter code

1. Open Visual Studio Code.

1. Open the Command Palette (**Ctrl+Shift+P**), run **Git: Clone**, and enter:

    ```
    https://github.com/microsoftlearning/mslearn-ai-language.git
    ```

    You may be prompted to confirm you trust the authors.

1. Open the cloned repo, then **File > Open Folder** and select `mslearn-ai-language/Labfiles/A-analyze-and-translate-text/Python`. This single folder holds the starter code for **every** task in this lab - you use one virtual environment and one `.env` throughout.

1. In Visual Studio Code, view the **Extensions** pane; and if it is not already installed, install the **Python** extension.

1. Right-click **requirements.txt** and choose **Open in Integrated Terminal**. Then create a virtual environment and install packages:

    ```
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

    > **Note**: Opening the terminal this way in Visual Studio Code automatically activates the Python environment. You may need to enable running scripts on your system.

## Configure your environment

The starter folder contains a **.env.example** file listing every setting this lab uses.

1. Copy **.env.example** to a new file named **.env** in the same folder.

1. Fill in the values you need. All of them come from the Foundry portal page you left open:

    | Setting | Value | Used by |
    | --- | --- | --- |
    | `FOUNDRY_ENDPOINT` | Your project endpoint with the `/api/projects/{project_name}` suffix **removed**, so it ends at the `.com` domain: `https://{your-resource}.services.ai.azure.com` | Task 1 |
    | `TRANSLATOR_ENDPOINT` | The Azure AI services form of the same resource: `https://{your-resource}.cognitiveservices.azure.com/` | Task 2 |
    | `PROJECT_ENDPOINT` | The **full** project endpoint, including the `/api/projects/{project_name}` suffix | Task 3 |
    | `AGENT_NAME` | `guest-feedback-agent` (the agent you create in Task 3; the name is case-sensitive) | Task 3 |

    > **Important**: Those first two endpoints point at the same resource in two different
    > formats. Azure Language uses the `services.ai.azure.com` form; Azure Translator and
    > the Speech tools use the older `cognitiveservices.azure.com` form. Getting these
    > mixed up is the single most common cause of authentication errors in this lab.

1. Save the **.env** file.

## Sign in to Azure

Every task in this lab authenticates with `DefaultAzureCredential`, which uses your Azure
CLI sign-in.

1. In the terminal, sign in to Azure:

    ```powershell
    az login
    ```

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.

1. When prompted, follow the instructions to sign in. Then confirm the details of the subscription containing your Foundry resource.

## Check you're ready for a task

Each task needs specific values in your `.env`. Before starting a task, run the preflight
check from the `Labfiles/A-analyze-and-translate-text/Python` folder - the same folder you
opened in VS Code, where your terminal is already open. It reads your `.env` and tells you
what (if anything) is missing:

```
python ../setup/check_env.py --task 2
```

> **Tip**: The preflight check uses only the Python standard library, so it works even if
> you haven't run `pip install` yet or your `labenv` environment isn't activated. That
> makes it safe to run first when you jump straight into a task.

Swap `2` for the task number you're about to start. That's it - head to any task:

| Task | Page |
| --- | --- |
| Task 1 – Analyze guest reviews | [A1](A1-analyze-guest-reviews.md) |
| Task 2 – Translate guest feedback | [A2](A2-translate-guest-feedback.md) |
| Task 3 – Hand the job to an agent | [A3](A3-build-a-guest-feedback-agent.md) |
