---
lab:
    title: 'Develop an audio-enabled chat app'
    description: 'Learn how to use Azure AI Foundry to build a generative AI app that supports audio input.'
---

# Develop an audio-enabled chat app

In this exercise, you use the *Phi-4-multimodal-instruct* generative AI model to generate responses to prompts that include audio files. You'll develop an app that provides AI assistance for a produce supplier company by using Azure AI Foundry and the Azure AI Model Inference service to summarize voice messages left by customers.

This exercise takes approximately **30** minutes.

## Create an Azure AI Foundry project

Let's start by deploying a model in an Azure AI Foundry project.

1. In a web browser, open the [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the **Azure AI Foundry** logo at the top left to navigate to the home page, which looks similar to the following image:

    ![Screenshot of Azure AI Foundry portal.](../media/ai-foundry-home.png)

1. In the home page, in the **Explore models and capabilities** section, search for the `Phi-4-multimodal-instruct` model; which we'll use in our project.
1. In the search results, select the **Phi-4-multimodal-instruct** model to see its details, and then at the top of the page for the model, select **Use this model**.
1. When prompted to create a project, enter a valid name for your project and expand **Advanced options**.
1. Select **Customize** and specify the following settings for your hub:
    - **Azure AI Foundry resource**: *A valid name for your Azure AI Foundry resource*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: *Select any **AI Services supported location***\*

    > \* Some Azure AI resources are constrained by regional model quotas. In the event of a quota limit being exceeded later in the exercise, there's a possibility you may need to create another resource in a different region. You can check the latest regional availability for specific models in the [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-serverless-availability#region-availability)

1. Select **Create** and wait for your project to be created.

    It may take a few moments for the operation to complete. 

1. Select **Agree and Proceed** to agree to the model terms, then select **Deploy** to complete the Phi model deployment.

1. When your project is created, the model details will be opened automatically. Note  the name of your model deployment; which should be **Phi-4-multimodal-instruct**

1. In the navigation pane on the left, select **Overview** to see the main page for your project; which looks like this:

    > **Note**: If an *Insufficient permissions** error is displayed, use the **Fix me** button to resolve it.

    ![Screenshot of a Azure AI Foundry project overview page.](../media/ai-foundry-project.png)

## Create a client application

Now that you deployed a model, you can use the Azure AI Foundry and Azure AI Model Inference SDKs to develop an application that chats with it.

> **Tip**: You can choose to develop your solution using Python or Microsoft C#. Follow the instructions in the appropriate section for your chosen language.

### Prepare the application configuration

1. In the Azure AI Foundry portal, view the **Overview** page for your project.
1. In the **Project details** area, note the **Azure AI Foundry project endpoint**. You'll use this endpoint to connect to your project in a client application.
1. Open a new browser tab (keeping the Azure AI Foundry portal open in the existing tab). Then in the new tab, browse to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`; signing in with your Azure credentials if prompted.

    Close any welcome notifications to see the Azure portal home page.

1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment with no storage in your subscription.

    The cloud shell provides a command-line interface in a pane at the bottom of the Azure portal. You can resize or maximize this pane to make it easier to work in.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    **<font color="red">Ensure you've switched to the classic version of the cloud shell before continuing.</font>**

1. In the cloud shell pane, enter the following commands to clone the GitHub repo containing the code files for this exercise (type the command, or copy it to the clipboard and then right-click in the command line and paste as plain text):


    ```
    rm -r mslearn-ai-audio -f
    git clone https://github.com/MicrosoftLearning/mslearn-ai-language mslearn-ai-audio
    ```

    > **Tip**: As you paste commands into the cloudshell, the ouput may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. After the repo has been cloned, navigate to the folder containing the application code files:  

    **Python**

    ```
    cd mslearn-ai-audio/Labfiles/09-audio-chat/Python
    ```

    **C#**

    ```
    cd mslearn-ai-audio/Labfiles/09-audio-chat/C-sharp
    ```

1. In the cloud shell command line pane, enter the following command to install the libraries you'll use:

    **Python**

    ```
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-identity azure-ai-projects azure-ai-inference
    ```

    **C#**

    ```
    dotnet add package Azure.Identity
    dotnet add package Azure.AI.Projects --version 1.0.0-beta.9
    dotnet add package Azure.AI.Inference --version 1.0.0-beta.5
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

    The file should open in a code editor.

1. In the code file, replace the **your_project_endpoint** placeholder with the endpoint for your project (copied from the project **Overview** page in the Azure AI Foundry portal), and the **your_model_deployment** placeholder with the name you assigned to your Phi-4-multimodal-instruct model deployment.

1. After you replace the placeholders, in the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

### Write code to connect to your project and get a chat client for your model

> **Tip**: As you add code, be sure to maintain the correct indentation.

1. Enter the following command to edit the code file that has been provided:

    **Python**

    ```
    code audio-chat.py
    ```

    **C#**

    ```
    code Program.cs
    ```

1. In the code file, note the existing statements that have been added at the top of the file to import the necessary SDK namespaces. Then, Find the comment **Add references**, add the following code to reference the namespaces in the libraries you installed previously:

    **Python**

    ```python
    # Add references
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.inference.models import SystemMessage, UserMessage, TextContentItem
    ```

    **C#**

    ```csharp
    // Add references
    using Azure.Identity;
    using Azure.AI.Projects;
    using Azure.AI.Inference;
    ```

1. In the **main** function, under the comment **Get configuration settings**, note that the code loads the project connection string and model deployment name values you defined in the configuration file.

1. Find the comment **Initialize the project client**, add the following code to connect to your Azure AI Foundry project using the Azure credentials you are currently signed in with:

    **Python**

    ```python
    # Initialize the project client
    project_client = AIProjectClient(
        credential=DefaultAzureCredential(
             exclude_environment_credential=True,
             exclude_managed_identity_credential=True
         ),
         endpoint=project_connection,
    )
    ```

    **C#**

    ```csharp
    // Initialize the project client
    DefaultAzureCredentialOptions options = new() { 
        ExcludeEnvironmentCredential = true,
        ExcludeManagedIdentityCredential = true
    };
    var projectClient = new AIProjectClient(
        new Uri(project_connection),
        new DefaultAzureCredential(options));
    ```

1. Find the comment **Get a chat client**, add the following code to create a client object for chatting with your model:

    **Python**

    ```python
    # Get a chat client
    chat_client = project_client.inference.get_chat_completions_client()
    ```

    **C#**

    ```csharp
    // Get a chat client
    ChatCompletionsClient chat = projectClient.GetChatCompletionsClient();
    ```
    

### Write code to submit a URL-based audio-based prompt

1. In the code editor for the **audio-chat.py** file, in the loop section, under the comment **Get a response to audio input**, add the following code to submit a prompt that includes the following audio:

    <video controls src="../media/avocados.mp4" title="A request for avocados" width="150"></video>

    **Python**

    ```python
    # Get a response to audio input
    file_path = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/avocados.mp3"
    response = chat_client.complete(
        model=model_deployment,
        messages=[
            SystemMessage(system_message),
            UserMessage(
                [
                    TextContentItem(text=prompt),
                    {
                        "type": "audio_url",
                        "audio_url": {"url": file_path}
                    }
                ]
            )
        ]
    )
    print(response.choices[0].message.content)
    ```

    **C#**

    ```csharp
    // Get a response to audio input
    string audioUrl = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/avocados.mp3";
    var requestOptions = new ChatCompletionsOptions()
    {
        Model = model_deployment,
        Messages =
        {
            new ChatRequestSystemMessage(system_message),
            new ChatRequestUserMessage(
                new ChatMessageTextContentItem(prompt),
                new ChatMessageAudioContentItem(new Uri(audioUrl))),
        }
    };
    var response = chat.Complete(requestOptions);
    Console.WriteLine(response.Value.Content);
    ```

1. Use the **CTRL+S** command to save your changes to the code file. You can also close the code editor (**CTRL+Q**) if you like.

### Sign into Azure and run the app

1. In the cloud shell command-line pane, enter the following command to sign into Azure.

    ```
    az login
    ```

    **<font color="red">You must sign into Azure - even though the cloud shell session is already authenticated.</font>**

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.
    
1. When prompted, follow the instructions to open the sign-in page in a new tab and enter the authentication code provided and your Azure credentials. Then complete the sign in process in the command line, selecting the subscription containing your Azure AI Foundry hub if prompted.

1. In the cloud shell command-line pane, enter the following command to run the app:

    **Python**

    ```
    python audio-chat.py
    ```

    **C#**

    ```
    dotnet run
    ```

1. When prompted, enter the prompt 

    ```
    Can you summarize this customer's voice message?
    ```

1. Review the response.

### Use a different audio file

1. In the code editor for your app code, find the code you added previously under the comment **Get a response to audio input**. Then modify the code as follows to select a different audio file:

    <video controls src="../media/fresas.mp4" title="A request for strawberries" width="150"></video>

    **Python**

    ```python
    # Get a response to audio input
    file_path = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/fresas.mp3"
    response = chat_client.complete(
        model=model_deployment,
        messages=[
            SystemMessage(system_message),
            UserMessage(
                [
                    TextContentItem(text=prompt),
                    {
                        "type": "audio_url",
                        "audio_url": {"url": file_path}
                    }
                ]
            )
        ]
    )
    print(response.choices[0].message.content)
    ```

    **C#**

    ```csharp
    // Get a response to audio input
    string audioUrl = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/fresas.mp3";
    var requestOptions = new ChatCompletionsOptions()
    {
        Model = model_deployment,
        Messages =
        {
            new ChatRequestSystemMessage(system_message),
            new ChatRequestUserMessage(
                new ChatMessageTextContentItem(prompt),
                new ChatMessageAudioContentItem(new Uri(audioUrl))),
        }
    };
    var response = chat.Complete(requestOptions);
    Console.WriteLine(response.Value.Content);
    ```

1. Use the **CTRL+S** command to save your changes to the code file. You can also close the code editor (**CTRL+Q**) if you like.

1. In the cloud shell command line pane beneath the code editor, enter the following command to run the app:

    **Python**

    ```
    python audio-chat.py
    ```

    **C#**

    ```
    dotnet run
    ```

1. When prompted, enter the following prompt: 
    
    ```
    Can you summarize this customer's voice message? Is it time-sensitive?
    ```

1. Review the response. Then enter `quit` to exit the program.

    > **Note**: In this simple app, we haven't implemented logic to retain conversation history; so the model will treat each prompt as a new request with no context of the previous prompt.

1. You can continue to run the app, choosing different prompt types and trying different prompts. When you're finished, enter `quit` to exit the program.

    If you have time, you can modify the code to use a different system prompt and your own internet-accessible audio files.

    > **Note**: In this simple app, we haven't implemented logic to retain conversation history; so the model will treat each prompt as a new request with no context of the previous prompt.

## Summary

In this exercise, you used Azure AI Foundry and the Azure AI Inference SDK to create a client application uses a multimodal model to generate responses to audio.

## Clean up

If you've finished exploring Azure AI Foundry, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
