---
lab:
    title: 'Use speech-capable generative AI models'
    description: Implement speech functionality using generative AI.
    duration: 30
    level: 300
    islab: true
---

# Use speech-capable generative AI models

Increasingly, generative AI model capabilities are evolving beyond text-based language completion to support content in other formats - including audible speech.

In this exercise, you'll use generative AI models to support two common scenarios:

- Speech synthesis (text-to-speech) - generating speech output.
- Speech recognition (speech-to-text) - transcribing speech input.

While this exercise is based on Python, you can develop generative AI speech applications using multiple language-specific SDKs; including:

- [OpenAI SDK for Python](https://pypi.org/project/openai/)
- [OpenAI SDK for .NET](<https://www.nuget.org/packages/OpenAI>)
- [OpenAI SDK for JavaScript](https://www.npmjs.com/package/openai)

This exercise takes approximately **30** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting this exercise, ensure you have:

- An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account)
- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Python version **3.13.xx**](https://www.python.org/downloads/release/python-31312/) installed\*
- [Git](https://git-scm.com/install/) installed and configured
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli?view=azure-cli-latest) installed

> \* Python 3.14 is available, but some dependencies are not yet compiled for that release. The lab has been successfully tested with Python 3.13.12.

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the Foundry logo at the top left to navigate to the home page.

1. If it is not already enabled, in the tool bar the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name; expanding the **Advanced options** area to specify the following settings for your project:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select *East US 2* (For this exercises some models are only available in this location.)

1. Select **Create**. Wait for your project to be created. Then view its home page.

## Deploy models

To develop speech-enables apps, we're going to need speech-enabled models. Specifically, we need a model that can perform speech-generation, and a model that can process speech input.

### Deploy a speech-generation model

1. Now you're ready to **Start building**. Select **Find models** (or on the **Discover** page, select the **Models** tab) to view the Microsoft Foundry model catalog.
1. In the model catalog, search for `gpt-4o-mini-tts`.
1. Review the model card, and then deploy it using the default settings.
1. When the model has been deployed, view its details, noting that the **Target URI** and **Key** required to use it are available here (you'll need the Target URI later).

### Deploy a speech-recognition model

1. In the Foundry portal menu bar, select **Build**; and then view the **Models** page. Note that the *gpt-4o-mini-tts* model you deployed is listed.
1. Select **Deploy a base model, and search the catalog for `gpt-4o-mini-transcribe`.
1. Deploy a *gpt-4o-mini-transcribe* model using the default settings.
1. Return to the **Models** page and verify that both of the model you deployed are listed.
1. Select either of the models to view the Target URI you need to use in your code.

## Get the application files from GitHub

The initial application files you'll need to develop speech applications are provided in a GitHub repo.

1. Open Visual Studio Code.
1. Open the command palette (*Ctrl+Shift+P*) and use the `Git:clone` command to clone the `https://github.com/microsoftlearning/mslearn-ai-language` repo to a local folder (it doesn't matter which one). Then open it.

    You may be prompted to confirm you trust the authors.

1. In Visual Studio Code, view the **Extensions** pane; and if it is not already installed, install the **Python** extension.
1. In the **Command Palette**, use the command `python:select interpreter`. Then select an existing environment if you have one, or create a new **Venv** environment based on your Python 3.1x installation.

    > **Tip**: If you are prompted to install dependencies, you can install the ones in the *requirements.txt* file in the */Labfiles/03-gen-ai-speech/Python/generate-speech* folder; but it's OK if you don't - we'll install them later!

    > **Tip**: If you prefer to use the terminal, you can create your **Venv** environment with `python -m venv labenv`, then activate it with `\labenv\Scripts\activate`.

## Create a speech-generation app

1. After the repo has been cloned, in the Explorer pane, navigate to the folder containing the application code files at **/Labfiles/03-gen-ai-speech/Python/generate-speech**. The application files include:
    - **.env** (the application configuration file)
    - **requirements.txt** (the Python package dependencies that need to be installed)
    - **generate-speech.py** (the code file for the application)

### Configure your application

1. In the **Explorer** pane, right-click the **generate-speech** folder containing the application files, and select **Open in integrated terminal** (or open a terminal in the **Terminal** menu and navigate to the */Labfiles/03-gen-ai-speech/Python/generate-speech* folder.)

    > **Note**: Opening the terminal in Visual Studio Code will automatically activate the Python environment. You may need to enable running scripts on your system.

1. Ensure that the terminal is open in the **generate-speech** folder with the prefix **(.venv)** to indicate that the Python environment you created is active.
1. Install the OpenAI SDK package and other required packages by running the following command:

    ```
    pip install -r requirements.txt
    ```

1. In the **Explorer** pane, in the **generate-speech** folder, select the **.env** file to open it. Then update the configuration values to include the **Target URI** (endpoint) for your **gpt-4o-mini-tts** model.

    > **Tip**: Copy the Target URI from the model details page in the Foundry portal.

    Save the modified configuration file.

### Write code to use the model for speech-generation

1. In the **Explorer** pane, in the **generate-speech** folder, select the **generate-speech.py** file to open it.
1. Review the existing code. You will add code to use the OpenAI SDK to access your model.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces** and add the following code to import the namespace you will need to use the OpenAI SDK:

    ```python
   # import namespaces
   from openai import AzureOpenAI
   from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    ```

1. In the **main** function, note that code to load the endpoint from the configuration file has already been provided. Then find the comment **Create the Azure OpenAI client**, and add the following code to create a client for the OpenAI API:

    ```Python
   # Create the Azure OpenAI client
   token_provider = get_bearer_token_provider(                    
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )

   client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider = token_provider,
        api_version="2025-03-01-preview"
   )
    ```

1. Find the comment **Generate speech and save to file**, and add the following code to submit a prompt to the speech-generation model save the response as a file.

    ```Python
   # Generate speech and save to file
   with client.audio.speech.with_streaming_response.create(
                model=model_deployment,
                voice="alloy",
                input="My voice is my passport!",
                instructions="Speak in a serious tone.",
            ) as response:
        response.stream_to_file(speech_file_path)
    ```

1. Save the changes to the code file.

### Run the application

1. In the terminal pane, use the following command to sign into Azure.

    ```powershell
    az login
    ```

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.

1. When prompted, follow the instructions to sign into Azure. Then complete the sign in process in the command line, viewing (and confirming if necessary) the details of the subscription containing your Foundry resource.
1. After you have signed in, enter the following command to run the application:

    ```
   python generate-speech.py
    ```

1. Observe the output as the code generates the requested speech and saves it in a file. The code should also play the generated audio file.

## Create a speech-transcription app

1. In the Explorer pane, navigate to the folder containing the application code files at **/Labfiles/03-gen-ai-speech/Python/transcribe-speech**. The application files include:
    - **.env** (the application configuration file)
    - **requirements.txt** (the Python package dependencies that need to be installed)
    - **transcribe-speech.py** (the code file for the application)

### Configure your application

1. In the **Explorer** pane, right-click the **transcribe-speech** folder containing the application files, and select **Open in integrated terminal** (or in the existing terminal, navigate to the */Labfiles/03-gen-ai-speech/Python/transcribe-speech* folder.)

    > **Note**: Opening the terminal in Visual Studio Code will automatically activate the Python environment. You may need to enable running scripts on your system.

1. Ensure that the terminal is open in the **transcribe-speech** folder with the prefix **(.venv)** to indicate that the Python environment you created previously is active.
1. Install the OpenAI SDK package and other required packages by running the following command:

    ```
    pip install -r requirements.txt
    ```

    > **Note**: This step isn't actually necessary if you completed the previous part of this exercise, as botg apps use the same environment and have the same dependencies - but it won't do any harm!

1. In the **Explorer** pane, in the **transcribe-speech** folder, select the **.env** file to open it. Then update the configuration values to include the **Target URI** (endpoint) for your **gpt-4o-mini-transcribe** model.

    > **Tip**: Copy the Target URI from the model details page in the Foundry portal.

    Save the modified configuration file.

### Write code to use the model for speech-transcription

1. In the **Explorer** pane, in the **transcribe-speech** folder, select the **transcribe-speech.py** file to open it.
1. Review the existing code. You will add code to use the OpenAI SDK to access your model.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces** and add the following code to import the namespace you will need to use the OpenAI SDK:

    ```python
   # import namespaces
   from openai import AzureOpenAI
   from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    ```

1. In the **main** function, note that code to load the endpoint from the configuration file has already been provided. Then find the comment **Create the Azure OpenAI client**, and add the following code to create a client for the OpenAI API:

    ```Python
   # Create the Azure OpenAI client
   token_provider = get_bearer_token_provider(                    
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )

   client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider = token_provider,
        api_version="2025-03-01-preview"
   )
    ```

1. Find the comment **Call model to transcribe audio file**, and add the following code to submit an audio file to the speech-transcription model generate a transcript.

    ```Python
   # Call model to transcribe audio file
   audio_file = open(file_path, "rb")
   transcription = client.audio.transcriptions.create(
        model=model_deployment,
        file=audio_file,
        response_format="text"
   )
        
   print(transcription)
        
    ```

1. Save the changes to the code file.

### Run the application

1. In the terminal pane, use the following command to sign into Azure.

    ```powershell
    az login
    ```

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.

1. When prompted, follow the instructions to sign into Azure. Then complete the sign in process in the command line, viewing (and confirming if necessary) the details of the subscription containing your Foundry resource.
1. After you have signed in, enter the following command to run the application:

    ```
   python transcribe-speech.py
    ```

1. Observe the output as the code submits the audio file to the model for transcription and displays the results. The code should also play the audio file.

## Clean up

If you've finished exploring speech-enabled models in Foundry Tools, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Open the [Azure portal](https://portal.azure.com) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
