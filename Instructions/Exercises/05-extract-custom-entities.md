---
lab:
    title: 'Extract custom entities'
    module: 'Module 3 - Getting Started with Natural Language Processing'
---

# Extract custom entities

In addition to other natural language processing capabilities, Azure AI Language Service enables you to define custom entities, and extract instances of them from text.

To test the custom entity extraction, we'll create a model and train it through Azure AI Language Studio, then use a command line application to test it.

## Create an *Azure AI Language Service* resource

If you don't already have one in your subscription, you'll need to provision an **Azure AI Language service** resource. Additionally, use custom text classification, you need to enable the **Custom text classification & extraction** feature.

1. In a browser, open the [Azure portal](https://portal.azure.com?azure-portal=true), and sign in with your Microsoft account.
1. Select the **Create a resource** button, search for *Language*, and create an **Azure AI Language Service** resource. When asked about *Additional features*, select **Custom text classification & extraction**. Create the resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Select or create a resource group*
    - **Region**: *Choose any available region*
    - **Name**: *Enter a unique name*
    - **Pricing tier**: Select **F0** (*free*), or **S** (*standard*) if F is not available.
    - **Storage account**: New storage account:
      - **Storage account name**: *Enter a unique name*.
      - **Storage account type**: Standard LRS
    - **Responsible AI notice**: Selected.

1. Select **Review + create,** then select **Create** to provision the resource.
1. Wait for deployment to complete, and then go to the deployed resource.
1. View the **Keys and Endpoint** page. You will need the information on this page later in the exercise.

## Upload sample ads

After you've created the Azure AI Language Service and storage account, you'll need to upload example ads to train your model later.

1. In a new browser tab, download sample classified ads from `https://aka.ms/entity-extraction-ads` and extract the files to a folder of your choice.

2. In the Azure portal, navigate to the storage account you created, and select it.

3. In your storage account select **Configuration**, located below **Settings**, and screen enable the option to **Allow Blob anonymous access** then select **Save**.

4. Select **Containers** from the left menu, located below **Data storage**. On the screen that appears, select **+ Container**. Give the container the name `classifieds`, and set **Anonymous access level** to **Container (anonymous read access for containers and blobs)**.

    > **NOTE**: When you configure a storage account for a real solution, be careful to assign the appropriate access level. To learn more about each access level, see the [Azure Storage documentation](https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-configure).

5. After creating the container, select it and click the **Upload** button and upload the sample ads you downloaded.

## Create a custom named entity recognition project

Now you're ready to reate a custom named entity recognition project. This project provides a working place to build, train, and deploy your model.

> **NOTE**: You can also create, build, train, and deploy your model through the REST API.

1. In a new browser tab, open the Azure AI Language Studio portal at `https://language.cognitive.azure.com/` and sign in using the Microsoft account associated with your Azure subscription.
1. If prompted to choose a Language resource, select the following settings:

    - **Azure Directory**: The Azure directory containing your subscription.
    - **Azure subscription**: Your Azure subscription.
    - **Resource type**: Language.
    - **Language resource**: The Azure AI Language resource you created previously.

    If you are <u>not</u> prompted to choose a language resource, it may be because you have multiple Language resources in your subscription; in which case:

    1. On the bar at the top if the page, select the **Settings (&#9881;)** button.
    2. On the **Settings** page, view the **Resources** tab.
    3. Select the language resource you just created, and click **Switch resource**.
    4. At the top of the page, click **Language Studio** to return to the Language Studio home page

1. At the top of the portal, in the **Create new** menu, select *Custom named entity recognition**.

1. Create a mew project with the following settings:
    - **Connect storage**: *This  value is likely already filled. Change it to your storage account if it isn't already*
    - **Basic information**:
    - **Name**: `CustomEntityLab`
        - **Text primary language**: English (US)
        - **Does your dataset include documents that are not in the same language?** : *No*
        - **Description**: `Custom entities in classified ads`
    - **Container**:
        - **Blob store container**: classifieds
        - **Are your files labeled with classes?**: No, I need to label my files as part of this project

## Label your data

Now that your project is created, you need to label your data to train your model how to identity entities.

1. If the **Data labeling** page is not already open, in the pane on the left, select **Data labeling**. You'll see a list of the files you uploaded to your storage account.
1. On the right side, in the **Activity** pane, select **Add entity** and add a new entity named `ItemForSale`.
1.  Repeat the previous stept o create the following entities:
    - `Price`
    - `Location`
1. After you've created your three entities, select **Ad 1.txt** so you can read it.
1. In *Ad 1.txt*: 
    1. Highlight the text *face cord of firewood* and select the **ItemForSale** entity.
    1. Highlight the text *Denver, CO* and select the **Location** entity.
    1. Highlight the text *$90* and select the **Price** entity.
1.In the **Activity** pane, note that this document will be added to the dataset for training the model.
1. Us the **Next document** button to move to the next document, and continue assigning text to appropriate entities for the entire set of documents, adding them all to the training dataset.
1. When you have labeled the last document (*Ad 9.txt*), save the labels.

## Train your model

After you've labeled your data, you need to train your model.

1. Select **Training jobs** in the pane on the left.
2. Select **Start a training job**
3. Select the option to rain anew model named `ExtractAds`
4. Choose **Automatically split the testing set from training data**

    > **TIP**: In your own extraction projects, use the testing split that best suits your data. For more consistent data and larger datasets, the Azure AI Language Service will automatically split the testing set by percentage. With smaller datasets, it's important to train with the right variety of possible input documents.

5. Click **Train**

    > **IMPORTANT**: Training your model can sometimes take several minutes. You'll get a notification when it's complete.

## Evaluate your model

In real world applications, it's important to evaluate and improve your model to verify it's performing as you expect. Two pages on the left show you the details of your trained model, and any testing that failed.

Select **Model performance** on the left side menu, and select your `ExtractAds` model. There you can see the scoring of your model, performance metrics, and when it was trained. You'll be able to see if any testing documents failed, and these failures help you understand where to improve.

## Deploy your model

When you're satisfied with the training of your model, it's time to deploy it, which allows you to start extracting entities through the API.

1. In the left pane, select **Deploying a model**.
2. Select **Add deployment**, then enter the name `AdEntities` and select the **ExtractAds** model.
3. Click **Deploy** to deploy your model.

## Prepare to develop an app in Visual Studio Code

To test the text analytics capabilities of the Azure AI Language service, we'll use a simple PowerShell script in Visual Studio Code.

> **Tip**: If you have already cloned the **mslearn-ai-language** repo, open it in Visual Studio code. Otherwise, follow these steps to clone it to your development environment.

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a **Git: Clone** command to clone the `https://github.com/MicrosoftLearning/mslearn-ai-language` repository to a local folder (it doesn't matter which folder).
3. When the repository has been cloned, open the folder in Visual Studio Code.
4. Wait while additional files are installed to support the C# code projects in the repo.

    > **Note**: If you are prompted to add required assets to build and debug, select **Not Now**.

## Configure your application

Applications for both C# and Python have been provided, as well as a sample text file you'll use to test the summarization. Both apps feature the same functionality. First, you'll complete some key parts of the application to enable it to use your Azure AI Language resource.

1. In Visual Studio Code, in the **Explorer** pane, browse to the **Labfiles/04-text-classification** folder and expand the **CSharp** or **Python** folder depending on your language preference and the **classify-text** folder it contains. Each folder contains the language-specific files for an app into which you're you're going to integrate Azure AI Language text classification functionality.
1. Right-click the **classify-text** folder containing your code files and open an integrated terminal. Then install the Azure AI Language Text Analytics SDK package by running the appropriate command for your language preference:

    **C#**:

    ```
    dotnet add package Azure.AI.TextAnalytics --version 5.3.0
    ```

    **Python**:

    ```
    pip install azure-ai-textanalytics==5.3.0
    ```

1. In the **Explorer** pane, in the **classify-text** folder, open the configuration file for your preferred language

    - **C#**: appsettings.json
    - **Python**: .env
    
1. Update the configuration values to include the  **endpoint** and a **key** from the Azure Language resource you created (available on the **Keys and Endpoint** page for your Azure AI Language resource in the Azure portal). The fil should already contain the project and deployment names for your text classification model.
1. Save the configuration file.

## Add code to classify documents

Now you're ready to use the Azure AI Language service to classify documents.

1. Expand the **articles** folder in the **classify-text** folder to view the text articles that your application will classify.
1. In the **classify-text** folder, open the code file for the client application:

    - **C#**: Program.cs
    - **Python**: classify-text.py

1. Find the comment **Import namespaces**. Then, under this comment, add the following language-specific code to import the namespaces you will need to use the Text Analytics SDK:

    **C#**: Programs.cs

    ```csharp
    // import namespaces
    using Azure;
    using Azure.AI.TextAnalytics;
    ```

    **Python**: classify-text.py

    ```python
    # import namespaces
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient
    ```

1. In the **Main** function, note that code to load the Azure AI Language service endpoint and key and the project and deployment names from the configuration file has already been provided. Then find the comment **Create client using endpoint and key**, and add the following code to create a client for the Text Analysis API:

    **C#**: Programs.cs

    ```csharp
    // Create client using endpoint and key
    AzureKeyCredential credentials = new AzureKeyCredential(aiSvcKey);
    Uri endpoint = new Uri(aiSvcEndpoint);
    TextAnalyticsClient aiClient = new TextAnalyticsClient(endpoint, credentials);
    ```

    **Python**: text-analysis.py

    ```Python
    # Create client using endpoint and key
    credential = AzureKeyCredential(ai_key)
    ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    ```

1. in the **Main** function, note that the existing code reads all of the files in the **articles** folder and creates a list containing their contents. Then find the comment **Get Classifications** and add the following code:

    **C#**: Program.cs

    ```csharp
    // Get Classifications
    ClassifyDocumentOperation operation = await aiClient.SingleLabelClassifyAsync(WaitUntil.Completed, batchedDocuments, projectName, deploymentName);

    int fileNo = 0;
    await foreach (ClassifyDocumentResultCollection documentsInPage in operation.Value)
    {
        
        foreach (ClassifyDocumentResult documentResult in documentsInPage)
        {
            Console.WriteLine(files[fileNo].Name);
            if (documentResult.HasError)
            {
                Console.WriteLine($"  Error!");
                Console.WriteLine($"  Document error code: {documentResult.Error.ErrorCode}");
                Console.WriteLine($"  Message: {documentResult.Error.Message}");
                continue;
            }

            Console.WriteLine($"  Predicted the following class:");
            Console.WriteLine();

            foreach (ClassificationCategory classification in documentResult.ClassificationCategories)
            {
                Console.WriteLine($"  Category: {classification.Category}");
                Console.WriteLine($"  Confidence score: {classification.ConfidenceScore}");
                Console.WriteLine();
            }
            fileNo++;
        }
    }
    ```
    
    **Python**: classify-text.py

    ```Python
    # Get Classifications
    operation = ai_client.begin_single_label_classify(
        batchedDocuments,
        project_name=project_name,
        deployment_name=deployment_name
    )

    document_results = operation.result()

    for doc, classification_result in zip(files, document_results):
        if classification_result.kind == "CustomDocumentClassification":
            classification = classification_result.classifications[0]
            print("{} was classified as '{}' with confidence score {}.".format(
                doc, classification.category, classification.confidence_score)
            )
        elif classification_result.is_error is True:
            print("{} has an error with code '{}' and message '{}'".format(
                doc, classification_result.error.code, classification_result.error.message)
            )
    ```

1. Save the changes to your code file.

## Test your application

Now your application is ready to test.

1. In the integrated terminal for the **classify-text** folder, and enter the following command to run the program:

    - **C#**: `dotnet run`
    - **Python**: `python classify-text.py`

    > **Tip**: You can use the **Maximize panel size** (**^**) icon in the terminal toolbar to see more of the console text.

1. Observe the output. The application should list a classification and confidence score for each text file.

## Clean up

When you don't need your project anymore, you can delete if from your **Projects** page in Language Studio. You can also remove the Azure AI Language service and associated storage account in the [Azure portal](https://portal.azure.com).
