---
lab:
    title: 'Translate Speech'
    description: "Translate language speech to speech and implement in your own app."
---

# Translate Speech

Azure AI Speech includes a speech translation API that you can use to translate spoken language. For example, suppose you want to develop a translator application that people can use when traveling in places where they don't speak the local language. They would be able to say phrases such as "Where is the station?" or "I need to find a pharmacy" in their own language, and have it translate them to the local language.

> **NOTE**
> This exercise is designed to be completed in the Azure cloud shell, where direct access to your computer's sound hardware is not supported. The lab will therefore use audio files for speech input and output streams. The code to achieve the same results using a mic and speaker is provided for your reference.

## Create an Azure AI Foundry project

Let's start by creating an Azure AI Foundry project.

1. In a web browser, open the [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the **Azure AI Foundry** logo at the top left to navigate to the home page, which looks similar to the following image:

    ![Screenshot of Azure AI Foundry portal.](../media/ai-foundry-home.png)

1. In the home page, select **+ Create project**.
1. In the **Create a project** wizard, enter a suitable project name for (for example, `my-ai-project`) then review the Azure resources that will be automatically created to support your project.
1. Select **Customize** and specify the following settings for your hub:
    - **Hub name**: *A unique name - for example `my-ai-hub`*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create a new resource group with a unique name (for example, `my-ai-resources`), or select an existing one*
    - **Location**: Choose any available region
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new AI Services resource with an appropriate name (for example, `my-ai-services`) or use an existing one*
    - **Connect Azure AI Search**: Skip connecting

1. Select **Next** and review your configuration. Then select **Create** and wait for the process to complete.
1. When your project is created, close any tips that are displayed and review the project page in Azure AI Foundry portal, which should look similar to the following image:

    ![Screenshot of a Azure AI project details in Azure AI Foundry portal.](../media/ai-foundry-project.png)

## Prepare to develop an app in Cloud Shell

1. In the Azure AI Foundry portal, view the **Overview** page for your project.
1. In the **Endpoint and keys** area, note the API key and the **location** under **Project details** for your project. You'll use the key and location to connect to the Azure AI Services Speech endpoint.
1. Open a new browser tab (keeping the Azure AI Foundry portal open in the existing tab). Then in the new tab, browse to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`; signing in with your Azure credentials if prompted.
1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    > **Tip**: As you paste commands into the cloudshell, the ouput may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. In the PowerShell pane, enter the following commands to clone the GitHub repo for this exercise:

    ```
   rm -r mslearn-ai-language -f
   git clone https://github.com/microsoftlearning/mslearn-ai-language mslearn-ai-language
    ```

    ***Now follow the steps for your chosen programming language.***

1. After the repo has been cloned, navigate to the folder containing the code files:  

    **Python**

    ```
   cd mslearn-ai-language/Labfiles/08b-speech-translation/Python/translator
    ```

    **C#**

    ```
   cd mslearn-ai-language/Labfiles/08b-speech-translation/C-Sharp/translator
    ```

1. In the cloud shell command line pane, enter the following command to install the libraries you'll use:

    **Python**

    ```
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-identity azure-ai-projects azure-cognitiveservices-speech==1.42.0
    ```

    **C#**

    ```
   dotnet add package Azure.Identity
   dotnet add package Azure.AI.Projects --prerelease
   dotnet add package Microsoft.CognitiveServices.Speech --version 1.42.0
    ```

1. Enter the following command to edit the configuration file that has been provided:

    **Python**

    ```
   code .env
    ```

    **C#**

    ```
   code appsettings.json
    ```

    The file is opened in a code editor.

1. In the code file, replace the **your_project_api_key** and **your_project_location** placeholders with the API key and location for your project (copied from the project **Overview** page in the Azure AI Foundry portal).
1. After you've replaced the placeholders, use the **CTRL+S** command to save your changes and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.

## Add code to use the Azure AI Speech SDK

> **Tip**: As you add code, be sure to maintain the correct indentation.

1. Enter the following command to edit the code file that has been provided:

    **Python**

    ```
   code translator.py
    ```

    **C#**

    ```
   code Program.cs
    ```

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces**. Then, under this comment, add the following language-specific code to import the namespaces you will need to use the Azure AI Speech SDK with the Azure AI Services resource in your Azure AI Foundry project:

    **Python**

    ```python
   # Import namespaces
   from azure.ai.projects.models import ConnectionType
   from azure.identity import DefaultAzureCredential
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.projects import AIProjectClient
   import azure.cognitiveservices.speech as speech_sdk
    ```

    **C#**

    ```csharp
   // Import namespaces
   using Azure.Identity;
   using Azure.AI.Projects;
   using Microsoft.CognitiveServices.Speech;
   using Microsoft.CognitiveServices.Speech.Audio;
   using Microsoft.CognitiveServices.Speech.Translation;
    ```

1. In the **main** function, under the comment **Get config settings**, note that the code loads the project API key and location you defined in the configuration file.

1. In the **Main** function, note that code to load the Azure AI Speech service key and region from the configuration file has already been provided. You must use these variables to create a **SpeechTranslationConfig** for your Azure AI Speech resource, which you will use to translate spoken input. Add the following code under the comment **Configure translation**:

    **Python**: translator.py

    ```python
    # Configure translation
    translation_config = speech_sdk.translation.SpeechTranslationConfig(project_key, location)
    translation_config.speech_recognition_language = 'en-US'
    translation_config.add_target_language('fr')
    translation_config.add_target_language('es')
    translation_config.add_target_language('hi')
    print('Ready to translate from',translation_config.speech_recognition_language)
    ```

    **C#**: Program.cs

    ```csharp
    // Configure translation
    translationConfig = SpeechTranslationConfig.FromSubscription(projectKey, location);
    translationConfig.SpeechRecognitionLanguage = "en-US";
    translationConfig.AddTargetLanguage("fr");
    translationConfig.AddTargetLanguage("es");
    translationConfig.AddTargetLanguage("hi");
    Console.WriteLine("Ready to translate from " + translationConfig.SpeechRecognitionLanguage);
    ```

1. You will use the **SpeechTranslationConfig** to translate speech into text, but you will also use a **SpeechConfig** to synthesize translations into speech. Add the following code under the comment **Configure speech**:

   **Python**

    ```python
   # Configure speech
   speech_config = speech_sdk.SpeechConfig(project_key, location)
   print('Ready to use speech service in:', speech_config.region)
    ```

    **C#**

    ```csharp
   // Configure speech
   speechConfig = SpeechConfig.FromSubscription(projectKey, location);
   Console.WriteLine("Ready to use speech service in " + speechConfig.Region);
    ```

1. Save your changes (*CTRL+S*), but leave the code editor open.

## Run the app

So far, the app doesn't do anything other than connect to your Azure AI Foundry project to retrieve the details needed to use the Speech service, but it's useful to run it and check that it works before adding speech functionality.

1. In the command line below the code editor, enter the following Azure CLI command to determine the Azure account that is signed in for the session:

    ```
   az account show
    ```

    The resulting JSON output should include details of your Azure account and the subscription you are working in (which should be the same subscription in which you created your Azure AI Foundry project.)

    Your app uses the Azure credentials for the context in which it's run to authenticate the connection to your project. In a production environment the app might be configured to run using a managed identity. In this development environment, it will use your authenticated cloud shell session credentials.

    > **Note**: You can sign into Azure in your development environment by using the `az login` Azure CLI command. In this case, the cloud shell has already logged in using the Azure credentials you signed into the portal with; so signing in explicitly is unnecessary. To learn more about using the Azure CLI to authenticate to Azure, see [Authenticate to Azure using Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli).

1. In the command line, enter the following language-specific command to run the translator app:

    **Python**

    ```
   python translator.py
    ```

    **C#**

    ```
   dotnet run
    ```

1. If you are using C#, you can ignore any warnings about using the **await** operator in asynchronous methods - we'll fix that later. The code should display the region of the speech service resource the application will use, a message that it is ready to translate from en-US and prompt you for a target language. A successful run indicates that the app has connected to your Azure AI Foundry project and retrieved the key it needs to use the Azure AI Speech service. Press ENTER to end the program.

## Implement speech translation

Now that you have a **SpeechTranslationConfig** for the Azure AI Speech service, you can use the Azure AI Speech translation API to recognize and translate speech.

1. In the **Main** function for your program, note that the code uses the **Translate** function to translate spoken input. Then in the **Translate** function, under the comment **Translate speech**, add the following code to create a **TranslationRecognizer** client that can be used to recognize and translate speech from a file.

    **Python**: translator.py

    ```python
    # Translate speech
    current_dir = os.getcwd()
    audioFile = current_dir + '/station.wav'
    audio_config_in = speech_sdk.AudioConfig(filename=audioFile)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config_in)
    print("Getting speech from file...")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations[targetLanguage]
    print(translation)
    ```

    **C#**: Program.cs

    ```csharp
    // Translate speech
    string audioFile = "station.wav";
    using AudioConfig audioConfig_in = AudioConfig.FromWavFileInput(audioFile);
    using TranslationRecognizer translator = new TranslationRecognizer(translationConfig, audioConfig_in);
    Console.WriteLine("Getting speech from file...");
    TranslationRecognitionResult result = await translator.RecognizeOnceAsync();
    Console.WriteLine($"Translating '{result.Text}'");
    translation = result.Translations[targetLanguage];
    Console.WriteLine(translation);
    ```

## Run the app

1. Save your changes (*CTRL+S*), and then in the command line below the code editor, enter the following command to run the program:

    **Python**

    ```
    python translator.py
    ```

    **C#**

    ```
    dotnet run
    ```

1. When prompted, enter a valid language code (*fr*, *es*, or *hi*). The program should transcribe your spoken input file and translate it to the language you specified (French, Spanish, or Hindi). Repeat this process, trying each language supported by the application.

> **NOTE**: The translation to Hindi may not always be displayed correctly in the Console window due to character encoding issues.

1. When you're finished, press ENTER to end the program.

> **NOTE**: The code in your application translates the input to all three languages in a single call. Only the translation for the specific language is displayed, but you could retrieve any of the translations by specifying the target language code in the **translations** collection of the result.

## Synthesize the translation to speech

So far, your application translates spoken input to text; which might be sufficient if you need to ask someone for help while traveling. However, it would be better to have the translation spoken aloud in a suitable voice.

Once again, due to the hardware limitations of the cloud shell we'll direct the synthesized speech output to a file.

1. In the **Translate** function, under the comment **Synthesize translation**, add the following code to use a **SpeechSynthesizer** client to synthesize the translation as speech and save it as a .wav file:

    **Python**: translator.py

    ```python
    # Synthesize translation
    output_file = "output.wav"
    voices = {
            "fr": "fr-FR-HenriNeural",
            "es": "es-ES-ElviraNeural",
            "hi": "hi-IN-MadhurNeural"
    }
    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
    audio_config_out = speech_sdk.audio.AudioConfig(filename=output_file)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config_out)
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    else:
        print("Spoken output saved in " + output_file)
    ```

    **C#**: Program.cs

    ```csharp
    // Synthesize translation
    var outputFile = "output.wav";
    var voices = new Dictionary<string, string>
                    {
                        ["fr"] = "fr-FR-HenriNeural",
                        ["es"] = "es-ES-ElviraNeural",
                        ["hi"] = "hi-IN-MadhurNeural"
                    };
    speechConfig.SpeechSynthesisVoiceName = voices[targetLanguage];
    using AudioConfig audioConfig_out = AudioConfig.FromWavFileOutput(outputFile);
    using SpeechSynthesizer speechSynthesizer = new SpeechSynthesizer(speechConfig, audioConfig_out);
    SpeechSynthesisResult speak = await speechSynthesizer.SpeakTextAsync(translation);
    if (speak.Reason != ResultReason.SynthesizingAudioCompleted)
    {
        Console.WriteLine(speak.Reason);
    }
    else
    {
        Console.WriteLine("Spoken output saved in " + outputFile);
    }
    ```

1. Save your changes (*CTRL+S*), and then in the command line below the code editor, enter the following command to run the program:

   **Python**

    ```
   python translator.py
    ```

    **C#**

    ```
   dotnet run
    ```

1. Review the output from the application, which should indicate that the spoken output translation was saved in a file. When you're finished, press **ENTER** to end the program.
1. If you have a media player capable of playing .wav audio files, in the toolbar for the cloud shell pane, use the **Upload/Download files** button to download the audio file from your app folder, and then play it:

    **Python**

    /home/*user*`/mslearn-ai-language/Labfiles/08b-speech-translation/Python/translator/output.wav`

    **C#**

    /home/*user*`/mslearn-ai-language/Labfiles/08b-speech-translation/C-Sharp/translator/output.wav`

> **NOTE**
> *In this example, you've used a **SpeechTranslationConfig** to translate speech to text, and then used a **SpeechConfig** to synthesize the translation as speech. You can in fact use the **SpeechTranslationConfig** to synthesize the translation directly, but this only works when translating to a single language, and results in an audio stream that is typically saved as a file.*

## Clean up

If you've finished exploring Azure AI Speech, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.

## What if you have a mic and speaker?

In this exercise, you used audio files for the speech input and output. Let's see how the code can be modified to use audio hardware.

### Using speech translation with a microphone

1. If you have a mic, you can use the following code to capture spoken input for speech translation:

    **Python**

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

    **C#**

    ```csharp
    // Translate speech
    using AudioConfig audioConfig_in = AudioConfig.FromDefaultMicrophoneInput();
    using TranslationRecognizer translator = new TranslationRecognizer(translationConfig, audioConfig_in);
    Console.WriteLine("Speak now...");
    TranslationRecognitionResult result = await translator.RecognizeOnceAsync();
    Console.WriteLine($"Translating '{result.Text}'");
    translation = result.Translations[targetLanguage];
    Console.WriteLine(translation);
    ```

> **Note**: The system default microphone is the default audio input, so you could also just omit the AudioConfig altogether!

### Using speech synthesis with a speaker

1. If you have a speaker, you can use the following code to synthesize speech.

    **Python**
    
    ```python
    # Synthesize translation
    voices = {
            "fr": "fr-FR-HenriNeural",
            "es": "es-ES-ElviraNeural",
            "hi": "hi-IN-MadhurNeural"
    }
    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
    audio_config_out = speech_sdk.audio.AudioConfig(use_default_speaker=True)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config_out)
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    ```
    
    **C#**
    
    ```csharp
    // Synthesize translation
    var voices = new Dictionary<string, string>
                    {
                        ["fr"] = "fr-FR-HenriNeural",
                        ["es"] = "es-ES-ElviraNeural",
                        ["hi"] = "hi-IN-MadhurNeural"
                    };
    speechConfig.SpeechSynthesisVoiceName = voices[targetLanguage];
    using AudioConfig audioConfig_out = AudioConfig.FromDefaultSpeakerOutput();
    using SpeechSynthesizer speechSynthesizer = new SpeechSynthesizer(speechConfig, audioConfig_out);
    SpeechSynthesisResult speak = await speechSynthesizer.SpeakTextAsync(translation);
    if (speak.Reason != ResultReason.SynthesizingAudioCompleted)
    {
        Console.WriteLine(speak.Reason);
    }
    ```

> **Note**: The system default speaker is the default audio output, so you could also just omit the AudioConfig altogether!

## More information

For more information about using the Azure AI Speech translation API, see the [Speech translation documentation](https://learn.microsoft.com/azure/ai-services/speech-service/speech-translation).
