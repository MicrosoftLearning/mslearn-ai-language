---
lab:
    title: 'Recognize and synthesize speech'
    description: Implement speech functionality using Azure Speech in Foundry Tools.
    duration: 30
    level: 300
    islab: true
---

# Recognize and synthesize speech

**Azure Speech in Foundry Tools** is a service that provides speech-related functionality, including:

- A *speech-to-text* API that enables you to implement speech recognition (converting audible spoken words into text).
- A *text-to-speech* API that enables you to implement speech synthesis (converting text into audible speech).

In this exercise, you'll use both of these APIs to implement a voice message assistant.

While this exercise is based on Python, you can develop speech applications using multiple language-specific SDKs; including:

- [Azure Speech SDK for Python](https://pypi.org/project/azure-cognitiveservices-speech/)
- [Azure Speech SDK for .NET](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech)
- [Azure Speech SDK for JavaScript](https://www.npmjs.com/package/microsoft-cognitiveservices-speech-sdk)

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
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*\*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select any available region

    > **TIP**: \* Remember the Foundry resource name - you'll need it later!

1. Wait for your project to be created. Then view the home page for your project.

## Get the application files from GitHub

The initial application files you'll need to develop the voice application are provided in a GitHub repo.

1. Open Visual Studio Code.
1. Open the command palette (*Ctrl+Shift+P*) and use the `Git:clone` command to clone the `https://github.com/microsoftlearning/mslearn-ai-language` repo to a local folder (it doesn't matter which one). Then open it.

    You may be prompted to confirm you trust the authors.

1. After the repo has been cloned, in the Explorer pane, navigate to the folder containing the application code files at **/Labfiles/04-azure-speech/Python/voice-mail**. The application files include:
    - **messages** (a subfolder containing audio recordings of messages)
    - **.env** (the application configuration file)
    - **requirements.txt** (the Python package dependencies that need to be installed)
    - **voice-mail.py** (the code file for the application)

## Configure your application

1. In Visual Studio Code, view the **Extensions** pane; and if it is not already installed, install the **Python** extension.
1. In the **Command Palette**, use the command `python:select interpreter`. Then select an existing environment if you have one, or create a new **Venv** environment based on your Python 3.1x installation.

    > **Tip**: If you are prompted to install dependencies, you can install the ones in the *requirements.txt* file in the */Labfiles/04-azure-speech/Python/voice-mail* folder; but it's OK if you don't - we'll install them later!

    > **Tip**: If you prefer to use the terminal, you can create your **Venv** environment with `python -m venv labenv`, then activate it with `\labenv\Scripts\activate`.

1. In the **Explorer** pane, right-click the **voice-mail** folder containing the application files, and select **Open in integrated terminal** (or open a terminal in the **Terminal** menu and navigate to the */Labfiles/04-azure-speech/Python/voice-mail* folder.)

    > **Note**: Opening the terminal in Visual Studio Code will automatically activate the Python environment. You may need to enable running scripts on your system.

1. Ensure that the terminal is open in the **voice-mail** folder with the prefix **(.venv)** to indicate that the Python environment you created is active.
1. Install the Azure AI Speech SDK package and other required packages by running the following command:

    ```
    pip install -r requirements.txt
    ```

1. In the **Explorer** pane, in the **voice-mail** folder, select the **.env** file to open it. Then update the configuration values to reflect the Cognitive Services **endpoint** for your Foundry resource.

    > **Important**: The endpoint should be *https://{YOUR_FOUNDRY_RESOURCE}.cognitiveservices.azure.com/*. The Foundry Resource name usually takes the form *{project_name}-resource*.

    Save the modified configuration file.

## Add code to synthesize speech

1. In the **Explorer** pane, in the **voice-mail** folder,  open the **voice-mail.py** file.
1. Review the existing code. You will add code to work with the Azure Speech SDK.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces** and add the following code to import the namespaces you will need to use the Speech SDK:

    ```python
   # import namespaces
   from azure.identity import DefaultAzureCredential
   import azure.cognitiveservices.speech as speech_sdk
    ```

1. In the **main** function, note that code to load the endpoint from the configuration file has already been provided. Then find the comment **Create speech_config using Entra ID authentication**, and add the following code to create a Speech Configuration object:

    ```Python
   # Create speech_config using Entra ID authentication
   credential = DefaultAzureCredential()
   speech_config = speech_sdk.SpeechConfig(    
        token_credential=credential,
        endpoint=foundry_endpoint)
    ```

1. Review the rest of the **main** function, and note that a loop has been implemented that enables the user to choose one of three options:
    1. Record a voice greeting
    1. Transcribe messages
    1. Exit the application

1. Find the **record_greeting** function, which you will implement to record a voice greeting as an audio file.
1. In the **record_greeting** function, find the comment **Synthesize the greeting message to an audio file**, and add the following code to synthesize speech from the text entered by the user and save it as an audio file.

    ```python
   output_file = "greeting.wav"
   audio_config = speech_sdk.audio.AudioOutputConfig(filename=output_file)

   speech_config.speech_synthesis_voice_name = "en-US-Serena:DragonHDLatestNeural"

   speech_synthesizer = speech_sdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
   )

   result = speech_synthesizer.speak_text_async(greeting_message).get()

   if result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Greeting recorded and saved to {output_file}")
        speech_synthesizer = None  # Release the synthesizer resources
   else:
        print("Error recording greeting: {}".format(result.reason))
    ```

1. Save the changes to the code file. Then, in the terminal pane, use the following command to sign into Azure.

    ```powershell
    az login
    ```

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.

1. When prompted, follow the instructions to sign into Azure. Then complete the sign in process in the command line, viewing (and confirming if necessary) the details of the subscription containing your Foundry resource.
1. After you have signed in, enter the following command to run the application:

    ```powershell
   python voice-mail.py
    ```

1. When prompted, enter **1** to record a greeting.
1. Enter a greeting, like `Hi. The person you called is not available right now. Leave a message.`
1. Wait while the speech is synthesized and saved as an audio file.

    You can select the *greeting.wav* file that is generated in the voice-mail folder to play it in Visual Studio Code.

## Add code to recognize speech

1. In the **voice-mail.py** code file, find the **transcribe_messages** function; which you will implement to transcribe each of the voice messages in the **messages** subfolder.

    The functional already contains code to loop through the files in the **messages** folder.

1. In the **transcribe_messages** function, find the comment **Transcribe the audio file**, and add the following code to transcribe the audio.

    ```python
   # Transcribe the audio file
   audio_config = speech_sdk.audio.AudioConfig(filename=file_path)
   speech_recognizer = speech_sdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
   )
   result = speech_recognizer.recognize_once_async().get()
   if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
        print(f"Transcription: {result.text}")
   else:
        print("Error transcribing message: {}".format(result.reason))
    ```

1. Save the changes to the code file. Then, in the terminal, enter the following command to run the application:

    ```powershell
   python voice-mail.py
    ```

1. When prompted, enter **2** to transcribe messages.
1. View the transcription for each message.

    Each file is played back automatically, so you can hear the message.

## Clean up

If you've finished exploring Azure Speech in Foundry Tools, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Open the [Azure portal](https://portal.azure.com) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.

## More information

For more information about using the **Speech-to-text** and **Text-to-speech** APIs, see the [Speech-to-text documentation](https://learn.microsoft.com/azure/ai-services/speech-service/index-speech-to-text) and [Text-to-speech documentation](https://learn.microsoft.com/azure/ai-services/speech-service/index-text-to-speech).
