---
lab:
    title: 'Translate text'
    description: Translate text with Azure Translator in Foundry Tools.
    duration: 20
    level: 300
---

# Translate text

**Azure Translator in Foundry Tools** is a service that enables you to translate text between languages. In this exercise, you'll use it to create a simple app that translates input in any supported language to the target language of your choice.

While this exercise is based on Python, you can develop text translation applications using multiple language-specific SDKs; including:

- [Azure Translator client library for Python](https://pypi.org/project/azure-ai-translation-text/)
- [Azure Translator client library for .NET](https://www.nuget.org/packages/Azure.AI.Translation.Text)
- [Azure Translator client library for JavaScript](https://www.npmjs.com/package/@azure-rest/ai-translation-text)

This exercise takes approximately **20** minutes.

## Prerequisites

Before starting this exercise, ensure you have:

- An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account)
- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Python version 3.13 or higher](https://www.python.org/downloads/) installed
- [Git](https://git-scm.com/install/) installed and configured

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the Foundry logo at the top left to navigate to the home page.

1. If it is not already enabled, in the tool bar the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name; expanding the **Advanced options** area to specify the following settings for your project:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select any of the **AI Foundry recommended** regions

    > **Tip**: Make a note of the region you selected. You'll need it later!

1. Select **Create**. Wait for your project to be created.
1. On the home page for your project, note the project endpoint, key, and OpenAI endpoint.

    > **TIP**: You're going to need the project key later!

## Get the application files from GitHub

The initial application files you'll need to develop the translation application are provided in a GitHub repo.

1. Open Visual Studio Code.
1. Open the command palette (*Ctrl+Shift+P*) and use the `Git:clone` command to clone the `https://github.com/microsoftlearning/mslearn-ai-language` repo to a local folder (it doesn't matter which one). Then open it.

    You may be prompted to confirm you trust the authors.

1. After the repo has been cloned, in the Explorer pane, navigate to the folder containing the application code files at **/Labfiles/03-translator/Python/translate-text**. The application files include:
    - **.env** (the application configuration file)
    - **requirements.txt** (the Python package dependencies that need to be installed)
    - **translate.py** (the code file for the application)

## Configure your application

1. In Visual Studio Code, view the **Extensions** pane; and if it is not already installed, install the **Python** extension.
1. In the **Command Palette**, use the command `python:select interpreter`. Then select an existing environment if you have one, or create a new **Venv** environment based on your Python 3.1x installation.

    > **Tip**: If you are prompted to install dependencies, you can install the ones in the *requirements.txt* file in the */Labfiles/03-translator/Python/translate-text* folder; but it's OK if you don't - we'll install them later!

1. In the **Explorer** pane, right-click the **translate-text** folder containing the application files, and select **Open in integrated terminal** (or open a terminal in the **Terminal** menu and navigate to the */Labfiles/03-translator/Python/translate-text* folder.)

    > **Note**: Opening the terminal in Visual Studio Code will automatically activate the Python environment. You may need to enable running scripts on your system.

1. Ensure that the terminal is open in the **translate-text** folder with the prefix **(.venv)** to indicate that the Python environment you created is active.
1. Install the Azure AI Language Text Analytics SDK package and other required packages by running the following command:

    ```
    pip install -r requirements.txt azure-ai-translation-text==1.0.1
    ```

1. In the **Explorer** pane, in the **translate-text** folder, select the **.env** file to open it. Then update the configuration values to include the **key** and **region** for your Foundry project.

    > **Important**:Be sure to add the *region* for your resource, <u>not</u> the endpoint!

    Save the modified configuration file.

## Add code to translate text

1. In the **Explorer** pane, in the **text-analysis** folder,  open the **translate.py** file.

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
   python translate.py
    ```

1. When prompted, enter a valid target language from the list displayed.
1. Enter a phrase to be translated (for example `This is a test` or `C'est un test`) and view the results, which should detect the source language and translate the text to the target language.
1. When you're done, enter `quit`. You can run the application again and choose a different target language.

## Clean up resources

If you're finished exploring Azure Translator, you can delete the resources you created in this exercise. Here's how:

1. Close the Azure cloud shell pane
1. In the Azure portal, browse to the Azure AI Translator resource you created in this lab.
1. On the resource page, select **Delete** and follow the instructions to delete the resource.

## More information

For more information about using **Azure Translator in Foundry Tools**, see the [Azure Translator in Foundry Tools documentation](https://learn.microsoft.com/azure/ai-services/translator/).
