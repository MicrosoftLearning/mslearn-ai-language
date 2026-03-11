---
lab:
  title: Translate text and speech
  description: Implement translation with Azure Translator and Azure Speech in Foundry Tools.
  duration: 30
  level: 300
  islab: true
  primarytopics:
    - Azure
---

# Translate text and speech

**Azure Translator in Foundry Tools** is a service that enables you to translate text between languages. Similarly, **Azure Speech in Foundry Tools** provides translation services for speech. In this exercise, you'll use them to create translation apps that translates input in any supported language to the target language of your choice.

While this exercise is based on Python, you can develop text translation applications using multiple language-specific SDKs; including:

- [Azure Translator client library for Python](https://pypi.org/project/azure-ai-translation-text/)
- [Azure Translator client library for .NET](https://www.nuget.org/packages/Azure.AI.Translation.Text)
- [Azure Translator client library for JavaScript](https://www.npmjs.com/package/@azure-rest/ai-translation-text)
- [Azure AI Speech SDK for Python](https://pypi.org/project/azure-cognitiveservices-speech/)
- [Azure AI Speech SDK for .NET](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech)
- [Azure AI Speech SDK for JavaScript](https://www.npmjs.com/package/microsoft-cognitiveservices-speech-sdk)

This exercise takes approximately **30** minutes.

## Prerequisites

Before starting this exercise, ensure you have:

- An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account)
- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Python version 3.13 or higher](https://www.python.org/downloads/) installed
- [Git](https://git-scm.com/install/) installed and configured

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the Foundry logo at the top left to navigate to the home page.

1. If it is not already enabled, in the tool bar the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name; expanding the **Advanced options** area to specify the following settings for your project:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select any available region

    > **Tip**: Make a note of the region you selected. You'll need it later!

1. Select **Create**. Wait for your project to be created.
1. On the home page for your project, note the project endpoint, key, and OpenAI endpoint.

    > **TIP**: You're going to need the project key later!

## Get the application files from GitHub

The initial application files you'll need to develop the translation application are provided in a GitHub repo.

1. Open Visual Studio Code.
1. Open the command palette (*Ctrl+Shift+P*) and use the `Git:clone` command to clone the `https://github.com/microsoftlearning/mslearn-ai-language` repo to a local folder (it doesn't matter which one). Then open it.

    You may be prompted to confirm you trust the authors.

1. In Visual Studio Code, view the **Extensions** pane; and if it is not already installed, install the **Python** extension.
1. In the **Command Palette**, use the command `python:select interpreter`. Then select an existing environment if you have one, or create a new **Venv** environment based on your Python 3.1x installation.

    > **Tip**: If you are prompted to install dependencies, you can install the ones in the *requirements.txt* file in the */Labfiles/07-translation/Python/translators* folder; but it's OK if you don't - we'll install them later!

    > **Tip**: If you prefer to use the terminal, you can create your **Venv** environment with `python -m venv labenv`, then activate it with `\labenv\Scripts\activate`.

## Create a text translation application

Now you're ready to use Azure Translator to implement text translation.

1. After the repo has been cloned, in the Explorer pane, navigate to the folder containing the application code files at **/Labfiles/07-translation/Python/translators**. The application files include:
    - **.env** (the application configuration file)
    - **requirements.txt** (the Python package dependencies that need to be installed)
    - **translate-text.py** (the code file for text-application)
    - **translate-speech.py** (the code file for speech-application)

### Configure your text translation application

1. In the **Explorer** pane, in the **translators** folder, select the **.env** file to open it. Then update the configuration values to include the **region** and **key** for your Foundry project.

    > **Important**:Be sure to add the *region* for your resource, <u>not</u> the endpoint!

    Save the modified configuration file.

1. In the **Explorer** pane, right-click the **translators** folder containing the application files, and select **Open in integrated terminal** (or open a terminal in the **Terminal** menu and navigate to the */Labfiles/07-translation/Python/translators* folder.)

    > **Note**: Opening the terminal in Visual Studio Code will automatically activate the Python environment. You may need to enable running scripts on your system.

1. Ensure that the terminal is open in the **translators** folder with the prefix **(.venv)** to indicate that the Python environment you created is active.
1. Install the Azure Translator SDK package and other required packages by running the following command:

    ```
    pip install -r requirements.txt azure-ai-translation-text==1.0.1
    ```

### Add code to translate text

1. In the **Explorer** pane, in the **translators** folder,  open the **translate-text.py** file.

1. Review the existing code. You will add code to work with Azure Translator.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces** and add the following code to import the namespaces you will need to use the Translator SDK:

    ```python
   # import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.translation.text import *
   from azure.ai.translation.text.models import InputTextItem
    ```

1. In the **main** function, note that the existing code reads the configuration settings.
1. Find the comment **Create client using endpoint and key** and add the following code:

    ```python
   # Create client using endpoint and key
   credential = AzureKeyCredential(translatorKey)
   client = TextTranslationClient(credential=credential, region=translatorRegion)
    ```

1. Find the comment **Choose target language** and add the following code, which uses the Text Translator service to return list of supported languages for translation, and prompts the user to select a language code for the target language:

    ```python
   # Choose target language
   languagesResponse = client.get_supported_languages(scope="translation")
   print("{} languages supported.".format(len(languagesResponse.translation)))
   print("(See https://learn.microsoft.com/azure/ai-services/translator/language-support#translation)")
   print("Enter a target language code for translation (for example, 'en'):")
   targetLanguage = "xx"
   supportedLanguage = False
   while supportedLanguage == False:
        targetLanguage = input()
        if  targetLanguage in languagesResponse.translation.keys():
            supportedLanguage = True
        else:
            print("{} is not a supported language.".format(targetLanguage))
    ```

1. Find the comment **Translate text** and add the following code, which repeatedly prompts the user for text to be translated, uses the Azure AI Translator service to translate it to the target language (detecting the source language automatically), and displays the results until the user enters *quit*:

    ```python
   # Translate text
   inputText = ""
   while inputText.lower() != "quit":
        inputText = input("Enter text to translate ('quit' to exit):")
        if inputText != "quit":
            input_text_elements = [InputTextItem(text=inputText)]
            translationResponse = client.translate(body=input_text_elements, to_language=[targetLanguage])
            translation = translationResponse[0] if translationResponse else None
            if translation:
                sourceLanguage = translation.detected_language
                for translated_text in translation.translations:
                    print(f"'{inputText}' was translated from {sourceLanguage.language} to {translated_text.to} as '{translated_text.text}'.")
    ```

1. Save your changes. Then, in the terminal pane, enter the following command to run the program:

    ```
   python translate-text.py
    ```

1. When prompted, enter a valid target language from the list in the link displayed.
1. Enter a phrase to be translated (for example `This is a test` or `C'est un test`) and view the results, which should detect the source language and translate the text to the target language.
1. When you're done, enter `quit`. You can run the application again and choose a different target language.

## Create a speech translation application

Now you're ready to use Azure Speech to implement text translation.

### Configure your speech translation application

1. In the **translators** folder, verify that the .env file contains the  **region** and **key** for your Foundry project (Azure Speech can use the same information as Azure Translator to connect to your Foundry resource).
1. Ensure that the terminal is open in the **translators** folder with the prefix **(.venv)** to indicate that the Python environment you created is active.
1. Install the Azure Speech SDK package and other required packages by running the following command:

    ```
    pip install -r requirements.txt azure-cognitiveservices-speech==1.48.2
    ```

### Add code to translate speech

1. In the **Explorer** pane, in the **translators** folder,  open the **translate-speech.py** file.

1. Review the existing code. You will add code to work with Azure Speech.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces** and add the following code to import the namespaces you will need to use the Speech SDK:

   ```python
   # Import namespaces
   from azure.core.credentials import AzureKeyCredential
   import azure.cognitiveservices.speech as speech_sdk
    ```

1. In the **main** function, under the comment **Get config settings**, note that the code loads the key and region you defined in the configuration file.

1. Find the following code under the comment **Configure translation**, and add the following code to configure your connection to the Azure AI Services Speech endpoint:

    ```python
   # Configure translation
   translation_config = speech_sdk.translation.SpeechTranslationConfig(speech_key, speech_region)
   translation_config.speech_recognition_language = 'en-US'
   translation_config.add_target_language('fr')
   translation_config.add_target_language('es')
   translation_config.add_target_language('hi')
   print('Ready to translate from',translation_config.speech_recognition_language)
    ```

1. You will use the **SpeechTranslationConfig** to translate speech into text, but you will also use a **SpeechConfig** to synthesize translations into speech. Add the following code under the comment **Configure speech**:

    ```python
   # Configure speech
   speech_config = speech_sdk.SpeechConfig(subscription=speech_key, region=speech_region)
   print('Ready to use speech service in:', speech_config.region)
    ```

1. In the code file, note that the code uses the **Translate** function to translate spoken input. Then in the **Translate** function, under the comment **Translate speech**, add the following code to create a **TranslationRecognizer** client that can be used to recognize and translate speech from the default system microphone.

    ```python
   # Translate speech
   audio_config_in = speech_sdk.AudioConfig(use_default_microphone=True)
   translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config_in)
   print("Speak now...")
   result = translator.recognize_once_async().get()
   print('Translating "{}"'.format(result.text))
   translation = result.translations[targetLanguage]
   print(translation)
    ```

1. In the **Translate** function, find the comment **Synthesize translation**, and add the following code to use a **SpeechSynthesizer** client to synthesize the translation as speech and play it through the default system speaker:

    ```python
   # Synthesize translation
   voices = {
            "fr": "fr-FR-HenriNeural",
            "es": "es-ES-ElviraNeural",
            "hi": "hi-IN-MadhurNeural"
   }
   speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
   audio_config_out = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
   speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config_out)
   speak = speech_synthesizer.speak_text_async(translation).get()
   if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    ```

1. Save your changes. Then, in the terminal pane, enter the following command to run the program:

    ```
   python translate-speech.py
    ```

1. When prompted, enter a valid language code (*fr*, *es*, or *hi*). Then, when prompted to speak, say something aloud (for example, "*Hello world!"*).

     The program shouldtranslate it to the language you specified (French, Spanish, or Hindi), and synthesize the translation.

    > **NOTE**: The code in your application translates the input to all three languages in a single call. Only the translation for the specific language is displayed, but you could retrieve any of the translations by specifying the target language code in the **translations** collection of the result.

    Repeat this process, trying each language supported by the application.

    > **NOTE**: The translation to Hindi may not always be displayed correctly in the terminal due to character encoding issues.

1. When you're finished, press ENTER to end the program.

## Clean up resources

If you have finished exploring Microsoft Foundry, delete any resources that you no longer need. This avoids accruing any unnecessary costs.

1. Open the **Azure portal** at [https://portal.azure.com](https://portal.azure.com) and select the resource group that contains the resources you created.
1. Select **Delete resource group** and then **enter the resource group name** to confirm. The resource group is then deleted.
