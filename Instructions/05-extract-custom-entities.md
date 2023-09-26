In addition to other natural language processing capabilities, Azure AI Language Service enables you to extract custom entities from various files.

To test the custom entity extraction, we'll create a model and train it through Azure AI Language Studio, then use a command line application to test it.

## Create an *Azure AI Language Service* resource

To use custom entity recognition, you'll need to create an Azure AI Language Service resource and select **Custom text classification & extraction** custom feature.

If you haven't already done so, create an **Azure AI Language Service** resource in your Azure subscription.

1. In a browser, open the [Azure portal](https://portal.azure.com?azure-portal=true), and sign in with your Microsoft account.
2. Select the **Create a resource** button, search for *Language*, and create an **Azure AI Language Service** resource. When asked about *Additional features*, select **Custom text classification & extraction**. Create the resource with the following settings:
    - **Subscription**: *Your Azure subscription*.
    - **Resource group**: *Select or create a resource group with a unique name*.
    - **Region**: *Choose any available region*:
    - **Name**: *Enter a unique name*.
    - **Pricing tier**: Standard S pricing tier
    - **Storage account**: New storage account
      - **Storage account name**: *Enter a unique name*.
      - **Storage account type**: Standard LRS
    - **Responsible AI notice**: Selected.

    > [!TIP]
    > You can reuse existing resources from previous labs if you have them available. Be sure to use a new container in the storage account to connect the custom entity extraction project to.

3. Review and create the resource.

### Get Azure AI Language resource key and endpoint

1. Navigate to the resource group in the [Azure portal](https://portal.azure.com?azure-portal=true), and select the Azure AI Language resource
2. Select **Keys and Endpoint** from the menu on the left side, located under **Resource Management**. You can copy it to your clipboard with the icon next to the key. We'll need one of the keys and the endpoint later, so either paste these values into Notepad for now or we'll come back to this page at that time.

## Upload sample ads

After you've created the Azure AI Language Service and storage account, you'll need to upload example ads to train your model later.

1. [Download sample classified ads](https://aka.ms/entity-extraction-ads) from this repo on GitHub. Extract the files from the `.zip` provided.

2. In the [Azure portal](https://portal.azure.com?azure-portal=true), navigate to the storage account you created, and select it

3. In your storage account, select **Containers** from the left menu, located below **Data storage**. On the screen that appears, select **+ Container**. Give the container a name `customner`, and set **Public access level** to *Container (anonymous read access for containers and blobs)*.

    > [!NOTE]
    > When you configure a storage account outside of this module, be careful to assign the appropriate access level. To learn more about each access level, see the [docs on Azure Storage](/azure/storage/blobs/anonymous-read-access-configure).

4. After creating the container, select it and click the **Upload** button to upload the sample ads you downloaded.

## Create a custom named entity recognition project

Once configuration is complete, create a custom named entity recognition project. This project provides a working place to build, train, and deploy your model.

> [!NOTE]
> You can also create, build, train, and deploy your model through the REST API

1. Log into the [Azure AI Language Studio](https://aka.ms/languageStudio) with your Azure account, and select the Azure subscription that you created your Azure AI Language resource in, and select your Azure AI Language resource

    > [!NOTE]
    > If you've previously logged into Azure AI Language Studio, it's already linked to your previous Azure AI Language resource. When creating the project in the following steps, be sure to switch that project to the correct resource.

2. Under the **Extract information** section, select **Custom named entity recognition**
3. Select **Create new project**
4. In the **Create a project** pop out, choose the following and create your project:
    - **Connect storage**: *This  value is likely already filled. Change resource to* customner *if it isn't already*
    - **Name**: customNERLab
    - **Description**: *Enter short description*
    - **Text primary language**: English (US)
    - **Blob store container**: customner
    - **Are your files labeled with classes?**: No, I need to label my files as part of this project

## Label your data

Now that your project is created, you need to label your data to train your model how to identity entities.

1. On the left, click on **Label data**. You'll see a list of the files you uploaded to your storage account.
2. On the right side, in the **Labeling** pane, click on **Add entity**. The files for this lab contain three you'll need to create: ItemForSale, Price, and Location

    ![Label data and add entity.](../media/tag-data-add-entity.png#lightbox)

3. After you've created your three entities, start by clicking on *Ad 1*. Here you can read the ad, specify the entity, and which dataset to assign it to.
4. Assign the entities for each ad to their respective values by selecting the beginning and end, which will then highlight the entity. Specify which entity it is.
5. Each file can specify the dataset; leave all to the default *Training* dataset.
6. Click **Save labels**

## Train your model

After you've labeled your data, you need to train your model.

1. Select **Training jobs** on the left side menu
3. Click **Start a training job**
4. Enter a name `ExtractAds`
5. Choose **Automatically split the testing set from training data**

    > [!TIP]
    > In your own extraction projects, use the testing split that best suits your data. For more consistent data and larger datasets, the Azure AI Language Service will automatically split the testing set by percentage. With smaller datasets, it's important to train with the right variety of possible input documents.

5. Click **Train**

> [!IMPORTANT]
> Training your model can sometimes take several minutes. You'll get a notification when it's complete.

## Evaluate your model

In real world applications, it's important to evaluate and improve your model to verify it's performing as you expect. Two pages on the left show you the details of your trained model, and any testing that failed.

1. Select **Model performance** on the left side menu, and select your `ExtractAds` model. There you can see the scoring of your model, performance metrics, and when it was trained. You'll be able to see if any testing documents failed, and these failures help you understand where to improve.

## Deploy your model

When you're satisfied with the training of your model, it's time to deploy it, which allows you to start extracting entities through the API.

1. On the left panel, select **Deploying a model**
2. Select **Add deployment**, then enter the name `customExtractAds` and select `ExtractAds` from the model drop-down
3. Click **Deploy** to deploy your model

## Send entity recognition task to your model

To test the text analytics capabilities of the Azure AI Language Service, we'll use a short command-line application that runs in the Cloud Shell on Azure.

### Run Cloud Shell

1. In the [Azure portal](https://portal.azure.com?azure-portal=true), select the **[>_]** (*Cloud Shell*) button at the top of the page to the right of the search box. A Cloud Shell pane will open at the bottom of the portal.

    ![Screenshot of starting Cloud Shell by clicking on the icon to the right of the top search box.](../media/powershell-portal-guide-1.png#lightbox)

2. The first time you open the Cloud Shell, you may be prompted to choose the type of shell you want to use (*Bash* or *PowerShell*). Select **PowerShell**. If you don't see this option, skip the step.  

3. If you're prompted to create storage for your Cloud Shell, ensure your subscription is specified and select **Create storage**. Then wait a minute or so for the storage to be created.

4. Make sure the type of shell indicated on the top left of the Cloud Shell pane is switched to *PowerShell*. If it's *Bash*, switch to *PowerShell* by using the drop-down menu.

5. Wait for PowerShell to start. You should see the following screen in the Azure portal:  

    ![Screenshot of waiting for PowerShell to start.](../media/powershell-prompt.png#lightbox)

### Configure and run PowerShell

Now that you have a custom model, you can run a client application that uses the Azure AI Language Service.

1. In the command shell, enter the following command to download the sample application and save it to a folder called ai-language.

    ```powershell
    git clone https://github.com/MicrosoftLearning/ai-language ai-language
    ```
  
    > [!TIP]
    > If you already used this command in another lab to clone the *ai-language* repository, you can skip this step.

2. The files are downloaded to a folder named **ai-language**. Now we want to see all of the files in your Cloud Shell storage and work with them. In the shell, enter the following commands:

    ```powershell
    cd ai-language/named-entity-recognition
    ```

    ```powershell
    code extract-entities.ps1
    ```

3. In `extract-entities.ps1`, note the top two lines of the script with places for your Azure AI Language Service key and endpoint, as well as your project and model names. Replace the placeholders for `$key` and `$endpoint` with your resource values (`$projectName`, and `$modelName` should match what you entered above), and save the file.

    > [!TIP]
    > If you don't have these values readily available, navigate to the [Azure portal](https://portal.azure.com?azure-portal=true), find the Azure AI Language resource you created earlier, and select the **Keys and endpoint** page on the left

4. Run the following command to call your model and extract the entities from the test file. Review the output.

    ```powershell
    .\extract-entities.ps1 test1.txt
    ```

    > [!NOTE]
    > You can update the script variable `$verbose` to `$true`to see the raw response JSON

5. Run the following command again, this time with a different file to extract. Review the output.

    ```powershell
    .\extract-entities.ps1 test2.txt
    ```

## Clean up

When you don't need your project anymore, you can delete if from your **Projects** page in Azure AI Language Studio. You can also remove the Azure AI Language Service and associated storage account in the [Azure portal](https://portal.azure.com?azure-portal=true).
