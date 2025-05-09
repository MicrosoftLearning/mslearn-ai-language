---
lab:
    title: 'Extract custom entities'
    description: "Train a model to extract customized entities from text input using Azure AI Language."
---

# Extract custom entities

In addition to other natural language processing capabilities, Azure AI Language Service enables you to define custom entities, and extract instances of them from text.

To test the custom entity extraction, we'll create a model and train it through Azure AI Language Studio, then use a command line application to test it.

## Provision an *Azure AI Language* resource

If you don't already have one in your subscription, you'll need to provision an **Azure AI Language service** resource. Additionally, use custom text classification, you need to enable the **Custom text classification & extraction** feature.

1. In a browser, open the Azure portal at `https://portal.azure.com`, and sign in with your Microsoft account.
1. Select the **Create a resource** button, search for *Language*, and create a **Language Service** resource. When on the page for *Select additional features*, select the custom feature containing **Custom named entity recognition extraction**. Create the resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Select or create a resource group*
    - **Region**: *Choose from one of the following regions*\*
        - Australia East
        - Central India
        - East US
        - East US 2
        - North Europe
        - South Central US
        - Switzerland North
        - UK South
        - West Europe
        - West US 2
        - West US 3
    - **Name**: *Enter a unique name*
    - **Pricing tier**: Select **F0** (*free*), or **S** (*standard*) if F is not available.
    - **Storage account**: New storage account:
      - **Storage account name**: *Enter a unique name*.
      - **Storage account type**: Standard LRS
    - **Responsible AI notice**: Selected.

1. Select **Review + create**, then select **Create** to provision the resource.
1. Wait for deployment to complete, and then go to the deployed resource.
1. View the **Keys and Endpoint** page. You will need the information on this page later in the exercise.

## Roles for your user
> **NOTE**: If you skip this step, you'll have a 403 error when trying to connect to your custom project. It's important that your current user has this role to access storage account blob data, even if you're the owner of the storage account.

1. Go to your storage account page in the Azure portal.
2. Select **Access Control (IAM)** in the left navigation menu.
3. Select **Add** to Add Role Assignments, and choose the **Storage Blob Data Contributor** role on the storage account.
4. Within **Assign access to**, select **User, group, or service principal**.
5. Select **Select members**.
6. Select your User. You can search for user names in the **Select** field.

## Upload sample ads

After you've created the Azure AI Language Service and storage account, you'll need to upload example ads to train your model later.

1. In a new browser tab, download sample classified ads from `https://aka.ms/entity-extraction-ads` and extract the files to a folder of your choice.

2. In the Azure portal, navigate to the storage account you created, and select it.

3. In your storage account select **Configuration**, located below **Settings**, and screen enable the option to **Allow Blob anonymous access** then select **Save**.

4. Select **Containers** from the left menu, located below **Data storage**. On the screen that appears, select **+ Container**. Give the container the name `classifieds`, and set **Anonymous access level** to **Container (anonymous read access for containers and blobs)**.

    > **NOTE**: When you configure a storage account for a real solution, be careful to assign the appropriate access level. To learn more about each access level, see the [Azure Storage documentation](https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-configure).

5. After creating the container, select it and click the **Upload** button and upload the sample ads you downloaded.

## Create a custom named entity recognition project

Now you're ready to create a custom named entity recognition project. This project provides a working place to build, train, and deploy your model.

> **NOTE**: You can also create, build, train, and deploy your model through the REST API.

1. In a new browser tab, open the Azure AI Language Studio portal at `https://language.cognitive.azure.com/` and sign in using the Microsoft account associated with your Azure subscription.
1. If prompted to choose a Language resource, select the following settings:

    - **Azure Directory**: The Azure directory containing your subscription.
    - **Azure subscription**: Your Azure subscription.
    - **Resource type**: Language.
    - **Language resource**: The Azure AI Language resource you created previously.

    If you are <u>not</u> prompted to choose a language resource, it may be because you have multiple Language resources in your subscription; in which case:

    1. On the bar at the top of the page, select the **Settings (&#9881;)** button.
    2. On the **Settings** page, view the **Resources** tab.
    3. Select the language resource you just created, and click **Switch resource**.
    4. At the top of the page, click **Language Studio** to return to the Language Studio home page.

1. At the top of the portal, in the **Create new** menu, select **Custom named entity recognition**.

1. Create a new project with the following settings:
    - **Connect storage**: *This  value is likely already filled. Change it to your storage account if it isn't already*
    - **Basic information**:
    - **Name**: `CustomEntityLab`
        - **Text primary language**: English (US)
        - **Does your dataset include documents that are not in the same language?** : *No*
        - **Description**: `Custom entities in classified ads`
    - **Container**:
        - **Blob store container**: classifieds
        - **Are your files labeled with classes?**: No, I need to label my files as part of this project

> **Tip**: If you get an error about not being authorized to perform this operation, you'll need to add a role assignment. To fix this, we add the role "Storage Blob Data Contributor" on the storage account for the user running the lab. More details can be found [on the documentation page](https://learn.microsoft.com/azure/ai-services/language-service/custom-named-entity-recognition/how-to/create-project?tabs=portal%2Clanguage-studio#enable-identity-management-for-your-resource)

## Label your data

Now that your project is created, you need to label your data to train your model how to identity entities.

1. If the **Data labeling** page is not already open, in the pane on the left, select **Data labeling**. You'll see a list of the files you uploaded to your storage account.
1. On the right side, in the **Activity** pane, select **Add entity** and add a new entity named `ItemForSale`.
1.  Repeat the previous step to create the following entities:
    - `Price`
    - `Location`
1. After you've created your three entities, select **Ad 1.txt** so you can read it.
1. In *Ad 1.txt*: 
    1. Highlight the text *face cord of firewood* and select the **ItemForSale** entity.
    1. Highlight the text *Denver, CO* and select the **Location** entity.
    1. Highlight the text *$90* and select the **Price** entity.
1. In the **Activity** pane, note that this document will be added to the dataset for training the model.
1. Use the **Next document** button to move to the next document, and continue assigning text to appropriate entities for the entire set of documents, adding them all to the training dataset.
1. When you have labeled the last document (*Ad 9.txt*), save the labels.

## Train your model

After you've labeled your data, you need to train your model.

1. Select **Training jobs** in the pane on the left.
2. Select **Start a training job**
3. Train a new model named `ExtractAds`
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

## Prepare to develop an app in Cloud Shell

To test the custom entity extraction capabilities of the Azure AI Language service, you'll develop a simple console application in Cloud Shell.

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
    cd mslearn-ai-language/Labfiles/05-custom-entity-recognition
    ```

## Configure your application

Applications for both C# and Python have been provided. Both apps feature the same functionality. First, you'll complete some key parts of the application to enable it to use your Azure AI Language resource.

1. Run the command `cd C-Sharp/custom-entities` or `cd Python/custom-entities` depending on your language preference. Each folder contains the language-specific files for an app into which you're going to integrate Azure AI Language text classification functionality.
1. Install the Azure AI Language Text Analytics SDK package by running the appropriate command for your language preference:

    **C#**:

    ```
    dotnet add package Azure.AI.TextAnalytics --version 5.3.0
    ```

    **Python**:

    ```
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-ai-textanalytics==5.3.0
    ```

1. Using the `ls` command, you can view the contents of the **custom-entities** folder. Note that it contains a file for configuration settings:

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

1. Update the configuration values to include the  **endpoint** and a **key** from the Azure Language resource you created (available on the **Keys and Endpoint** page for your Azure AI Language resource in the Azure portal).The file should already contain the project and deployment names for your custom entity extraction model.
1. After you've replaced the placeholders, within the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

## Add code to extract entities

Now you're ready to use the Azure AI Language service to extract custom entities from text.

1. Note that the **custom-entities** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: custom-entities.py

1. Open the code file and find the comment **Import namespaces**. Then, under this comment, add the following language-specific code to import the namespaces you will need to use the Text Analytics SDK:

    **C#**: Programs.cs

    ```csharp
    // import namespaces
    using Azure;
    using Azure.AI.TextAnalytics;
    ```

    **Python**: custom-entities.py

    ```python
    # import namespaces
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient
    ```

1. In the **Main** function, note that code to load the Azure AI Language service endpoint and key and the project and deployment names from the configuration file has already been provided. Then find the comment **Create client using endpoint and key**, and add the following code to create a client for the Text Analysis API:

    **C#**: Programs.cs

    ```csharp
    // Create client using endpoint and key
    AzureKeyCredential credentials = new(aiSvcKey);
    Uri endpoint = new(aiSvcEndpoint);
    TextAnalyticsClient aiClient = new(endpoint, credentials);
    ```

    **Python**: custom-entities.py

    ```Python
    # Create client using endpoint and key
    credential = AzureKeyCredential(ai_key)
    ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    ```

1. In the **Main** function, note that the existing code reads all of the files in the **ads** folder and creates a list containing their contents. In the case of the C# code, a list of **TextDocumentInput** objects is used to include the file name as an ID and the language. In Python a simple list of the text contents is used.
1. Find the comment **Extract entities** and add the following code:

    **C#**: Program.cs

    ```csharp
    // Extract entities
    RecognizeCustomEntitiesOperation operation = await aiClient.RecognizeCustomEntitiesAsync(WaitUntil.Completed, batchedDocuments, projectName, deploymentName);

    await foreach (RecognizeCustomEntitiesResultCollection documentsInPage in operation.Value)
    {
        foreach (RecognizeEntitiesResult documentResult in documentsInPage)
        {
            Console.WriteLine($"Result for \"{documentResult.Id}\":");

            if (documentResult.HasError)
            {
                Console.WriteLine($"  Error!");
                Console.WriteLine($"  Document error code: {documentResult.Error.ErrorCode}");
                Console.WriteLine($"  Message: {documentResult.Error.Message}");
                Console.WriteLine();
                continue;
            }

            Console.WriteLine($"  Recognized {documentResult.Entities.Count} entities:");

            foreach (CategorizedEntity entity in documentResult.Entities)
            {
                Console.WriteLine($"  Entity: {entity.Text}");
                Console.WriteLine($"  Category: {entity.Category}");
                Console.WriteLine($"  Offset: {entity.Offset}");
                Console.WriteLine($"  Length: {entity.Length}");
                Console.WriteLine($"  ConfidenceScore: {entity.ConfidenceScore}");
                Console.WriteLine($"  SubCategory: {entity.SubCategory}");
                Console.WriteLine();
            }

            Console.WriteLine();
        }
    }
    ```

    **Python**: custom-entities.py

    ```Python
    # Extract entities
    operation = ai_client.begin_recognize_custom_entities(
        batchedDocuments,
        project_name=project_name,
        deployment_name=deployment_name
    )

    document_results = operation.result()

    for doc, custom_entities_result in zip(files, document_results):
        print(doc)
        if custom_entities_result.kind == "CustomEntityRecognition":
            for entity in custom_entities_result.entities:
                print(
                    "\tEntity '{}' has category '{}' with confidence score of '{}'".format(
                        entity.text, entity.category, entity.confidence_score
                    )
                )
        elif custom_entities_result.is_error is True:
            print("\tError with code '{}' and message '{}'".format(
                custom_entities_result.error.code, custom_entities_result.error.message
                )
            )
    ```

1. Save the changes and close the code editor.

## Test your application

Now your application is ready to test.

1. Enter the following command to run the program:

    - **C#**: `dotnet run`
    - **Python**: `python custom-entities.py`

    > **Tip**: You can maximize the panel size in the terminal toolbar to see more of the console text.

1. Observe the output. The application should list details of the entities found in each text file.

## Clean up

When you don't need your project anymore, you can delete if from your **Projects** page in Language Studio. You can also remove the Azure AI Language service and associated storage account in the [Azure portal](https://portal.azure.com).
