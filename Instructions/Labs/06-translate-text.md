---
lab:
    title: 'Translate Text'
    description: "Translate provided text between any supported languages with Azure AI Translator."
---

# Translate Text

**Azure AI Translator** is a service that enables you to translate text between languages. In this exercise, you'll use it to create a simple app that translates input in any supported language to the target language of your choice.

## Provision an *Azure AI Translator* resource

If you don't already have one in your subscription, you'll need to provision an **Azure AI Translator** resource.

1. Open the Azure portal at `https://portal.azure.com`, and sign in using the Microsoft account associated with your Azure subscription.
1. In the search field at the top, search for **Translators** then select **Translators** in the results.
1. Create a resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group*
    - **Region**: *Choose any available region*
    - **Name**: *Enter a unique name*
    - **Pricing tier**: Select **F0** (*free*), or **S** (*standard*) if F is not available.
1. Select **Review + create**, then select **Create** to provision the resource.
1. Wait for deployment to complete, and then go to the deployed resource.
1. View the **Keys and Endpoint** page. You will need the information on this page later in the exercise.

## Prepare to develop an app in Cloud Shell
You'll develop your text translation app using Cloud Shell. The code files for your app have been provided in a GitHub repo.

> **Tip**: If you have already cloned the **mslearn-ai-language** repo, you can skip this task. Otherwise, follow these steps to clone it to your development environment.

1. In the Azure Portal, use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    > **Tip**: As you paste commands into the cloudshell, the ouput may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. In the PowerShell pane, enter the following commands to clone the GitHub repo for this exercise:

    ```
    rm -r mslearn-ai-language -f
    git clone https://github.com/microsoftlearning/mslearn-ai-language mslearn-ai-language
    ```

1. After the repo has been cloned, navigate to the folder containing the application code files:  

    ```
    cd mslearn-ai-language/Labfiles/06b-translator-sdk
    ```

## Configure your application

Applications for both C# and Python have been provided. Both apps feature the same functionality. First, you'll complete some key parts of the application to enable it to use your Azure AI Translator resource.

1. Run the command `cd C-Sharp/translate-text` or `cd Python/translate-text` depending on your language preference. Each folder contains the language-specific code files for an app into which you're you're going to integrate Azure AI Translator functionality.
1. Install the Azure AI Translator SDK package by running the appropriate command for your language preference:

    **C#**:

    ```
    dotnet add package Azure.AI.Translation.Text --version 1.0.0
    ```

    **Python**:

    ```
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-ai-translation-text==1.0.0
    ```

1. Using the `ls` command, you can view the contents of the **translate-text** folder. Note that it contains a file for configuration settings:

    - **C#**: appsettings.json
    - **Python**: .env

1. Enter the following command to edit the configuration file that has been provided:

    **C#**

    ```
   code appsettings.json
    ```

    **Python**

    ```
   code .env
    ```

    The file is opened in a code editor.

1. Update the configuration values to include the  **region** and a **key** from the Azure AI Translator resource you created (available on the **Keys and Endpoint** page for your Azure AI Translator resource in the Azure portal).

    > **NOTE**: Be sure to add the *region* for your resource, <u>not</u> the endpoint!

1. After you've replaced the placeholders, within the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

## Add code to translate text

Now you're ready to use Azure AI Translator to translate text.

1. Note that the **translate-text** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: translate.py

    Open the code file and at the top, under the existing namespace references, find the comment **Import namespaces**. Then, under this comment, add the following language-specific code to import the namespaces you will need to use the Text Analytics SDK:

    **C#**: Programs.cs

    ```csharp
    // import namespaces
    using Azure;
    using Azure.AI.Translation.Text;
    ```

    **Python**: translate.py

    ```python
    # import namespaces
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.translation.text import *
    from azure.ai.translation.text.models import InputTextItem
    ```

1. In the **Main** function, note that the existing code reads the configuration settings.
1. Find the comment **Create client using endpoint and key** and add the following code:

    **C#**: Programs.cs

    ```csharp
    // Create client using endpoint and key
    AzureKeyCredential credential = new(translatorKey);
    TextTranslationClient client = new(credential, translatorRegion);
    ```

    **Python**: translate.py

    ```python
    # Create client using endpoint and key
    credential = AzureKeyCredential(translatorKey)
    client = TextTranslationClient(credential=credential, region=translatorRegion)
    ```

1. Find the comment **Choose target language** and add the following code, which uses the Text Translator service to return  list of supported languages for translation, and prompts the user to select a language code for the target language.

    **C#**: Programs.cs

    ```csharp
    // Choose target language
    Response<GetSupportedLanguagesResult> languagesResponse = await client.GetSupportedLanguagesAsync(scope:"translation").ConfigureAwait(false);
    GetSupportedLanguagesResult languages = languagesResponse.Value;
    Console.WriteLine($"{languages.Translation.Count} languages available.\n(See https://learn.microsoft.com/azure/ai-services/translator/language-support#translation)");
    Console.WriteLine("Enter a target language code for translation (for example, 'en'):");
    string targetLanguage = "xx";
    bool languageSupported = false;
    while (!languageSupported)
    {
        targetLanguage = Console.ReadLine();
        if (languages.Translation.ContainsKey(targetLanguage))
        {
            languageSupported = true;
        }
        else
        {
            Console.WriteLine($"{targetLanguage} is not a supported language.");
        }

    }
    ```

    **Python**: translate.py

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

1. Find the comment **Translate text** and add the following code, which repeatedly prompts the user for text to be translated, uses the Azure AI Translator service to translate it to the target language (detecting the source language automatically), and displays the results until the user enters *quit*.

    **C#**: Programs.cs

    ```csharp
    // Translate text
    string inputText = "";
    while (inputText.ToLower() != "quit")
    {
        Console.WriteLine("Enter text to translate ('quit' to exit)");
        inputText = Console.ReadLine();
        if (inputText.ToLower() != "quit")
        {
            Response<IReadOnlyList<TranslatedTextItem>> translationResponse = await client.TranslateAsync(targetLanguage, inputText).ConfigureAwait(false);
            IReadOnlyList<TranslatedTextItem> translations = translationResponse.Value;
            TranslatedTextItem translation = translations[0];
            string sourceLanguage = translation?.DetectedLanguage?.Language;
            Console.WriteLine($"'{inputText}' translated from {sourceLanguage} to {translation?.Translations[0].TargetLanguage} as '{translation?.Translations?[0]?.Text}'.");
        }
    } 
    ```

    **Python**: translate.py

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

1. Save the changes to your code file and close the code editor.

## Test your application

Now your application is ready to test.

1. Enter the following command to run the program:

    - **C#**: `dotnet run`
    - **Python**: `python translate.py`

    > **Tip**: You can maximize the panel size in the terminal toolbar to see more of the console text.

1. When prompted, enter a valid target language from the list displayed.
1. Enter a phrase to be translated (for example `This is a test` or `C'est un test`) and view the results, which should detect the source language and translate the text to the target language.
1. When you're done, enter `quit`. You can run the application  again and choose a different target language.

## Clean up

When you don't need your project anymore, you can delete the Azure AI Translator resource in the [Azure portal](https://portal.azure.com).
