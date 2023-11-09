---
lab:
    title: 'Custom text classification'
    module: 'Module 3 - Getting Started with Natural Language Processing'
---

Azure AI Language provides several NLP capabilities, including the key phrase identification, text summarization, and sentiment analysis. The Language service also provides custom features like custom question answering and custom text classification.

To test the custom text classification of the Azure AI Language service, we'll configure the model using Language Studio then use a small command-line application that runs in the Cloud Shell to test it. The same pattern and functionality used here can be followed for real-world applications.

## Create an Azure AI Language service resource

If you don't already have one in your subscription, you'll need to provision an **Azure AI Language service** resource. Additionally, use custom text classification, you need to enable the **Custom text classification & extraction** feature.

1. In a browser, open the [Azure portal](https://portal.azure.com?azure-portal=true), and sign in with your Microsoft account.
1. Select the search field at the top of the portal, search for **Azure AI services**, and create a **Language Service** resource.
1. Select the box that includes **Custom text classification**. Then select **Continue to create your resource**.
1. Create a resource with the following settings:
    - **Subscription**: *Your Azure subscription*.
    - **Resource group**: *Select or create a resource group*.
    - **Region**: *Choose any available region*:
    - **Name**: *Enter a unique name*.
    - **Pricing tier**: Select **F0** (*free*), or **S** (*standard*) if F is not available.
    - **Storage account**: New storage account
      - **Storage account name**: *Enter a unique name*.
      - **Storage account type**: Standard LRS
    - **Responsible AI notice**: Selected.

1. Select **Review + create,** then select **Create** to provision the resource.
1. Wait for deployment to complete, and then go to the deployed resource.
1. View the **Keys and Endpoint** page. You will need the information on this page later in the exercise.

## Upload sample articles

Once you've created the Azure AI Language service and storage account, you'll need to upload example articles to train your model later.

1. In a new browser tab, download sample articles from `https://aka.ms/classification-articles` and extract the files to a folder of your choice.

1. In the Azure portal, navigate to the storage account you created, and select it.

1. In your storage account select **Configuration**, located below **Settings**. In the Configuration screen enable the option to **Allow Blob anonymous access** then select **Save**.

1. Select **Containers** in the left menu, located below **Data storage**. On the screen that appears, select **+ Container**. Give the container the name `articles`, and set **Anonymous access level** to **Container (anonymous read access for containers and blobs)**.

    > **NOTE**
    > When you configure a storage account for a real solution, be careful to assign the appropriate access level. To learn more about each access level, see the [Azure Storage documentation](https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-configure).

1. After you've created the container, select it then select the **Upload** button. Select **Browse for files** to browse for the sample articles you downloaded. Then select **Upload**.

## Create a custom text classification project

After configuration is complete, create a custom text classification project. This project provides a working place to build, train, and deploy your model.

> **NOTE**
> This lab utilizes **Language Studio**, but you can also create, build, train, and deploy your model through the REST API.

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

1. Under the **Classify text** tab, select **Custom text classification**.
1. Select **+ Create new project**.
1. The **Connect storage** page appears. All values will already have been filled. So select **Next**.
1. On the **Select project type** page, select **Single label classification**. Then select **Next**.
1. On the **Enter basic information** pane, set the following:
    - **Name**: `ClassifyLab`  
    - **Text primary language**: English (US)
    - **Description**: `Custom text lab`

1. Select **Next**.
1. On the **Choose container** page, set the **Blob store container** dropdown to your *articles* container.
1. Select the  **No, I need to label my files as part of this project** option. Then select **Next**.
1. Select **Create project**.

## Label your data

Now that your project is created, you need to label, or tag, your data to train your model how to classify text.

1. On the left, select **Data labeling**, if not already selected. You'll see a list of the files you uploaded to your storage account.
1. On the right side, in the **Activity** pane, select **+ Add class**.  The articles in this lab fall into four classes you'll need to create: `Classifieds`, `Sports`, `News`, and `Entertainment`.

    ![Screenshot showing the tag data page and the add class button.](../media/tag-data-add-class-new.png#lightbox)

1. After you've created your four classes, select **Article 1** to start. Here you can read the article, define which class this file is, and which dataset to assign it to.
1. Assign each article the appropriate class and dataset (training or testing) using the **Activity** pane on the right.  You can select a label from the list of labels on the right, and set each article to training or testing using the options at the bottom of the Activity pane. You  select **Next document** to move to the next document. For the purposes of this lab, we'll define which are to be used for training the model and testing the model:

    | Article  | Class  | Dataset  |
    |---------|---------|---------|
    | Article 1 | Sports | Training |
    | Article 10 | News | Training |
    | Article 11 | Entertainment | Testing |
    | Article 12 | News | Testing |
    | Article 13 | Sports | Testing |
    | Article 2 | Sports | Training |
    | Article 3 | Classifieds | Training |
    | Article 4 | Classifieds | Training |
    | Article 5 | Entertainment | Training |
    | Article 6 | Entertainment | Training |
    | Article 7 | News | Training |
    | Article 8 | News | Training |
    | Article 9 | Entertainment | Training |

    > **NOTE**
    > Files in Language Studio are listed alphabetically, which is why the above list is not in sequential order. Make sure you visit both pages of documents when labeling your articles.

1. Select **Save labels** to save your labels.

## Train your model

After you've labeled your data, you need to train your model.

1. Select **Training jobs** on the left side menu.
1. Select **Start a training job**.
1. Train a new model named `ClassifyArticles`.
1. Select **Use a manual split of training and testing data**.

    > **TIP**
    > In your own classification projects, the Azure AI Language service will automatically split the testing set by percentage which is useful with a large dataset. With smaller datasets, it's important to train with the right class distribution.

1. Select **Train**

> **IMPORTANT**
> Training your model can sometimes take several minutes. You'll get a notification when it's complete.

## Evaluate your model

In real world applications of text classification, it's important to evaluate and improve your model to verify it's performing as you expect.

1. Select **Model performance**, and select your **ClassifyArticles** model. There you can see the scoring of your model, performance metrics, and when it was trained. If the scoring of your model isn't 100%, it means that one of the documents used for testing didn't evaluate to what it was labeled. These failures can help you understand where to improve.
1. Select **Test set details** tab. If there are any errors, this tab allows you to see the articles you indicated for testing and what the model predicted them as and whether that conflicts with their test label. The tab defaults to show incorrect predictions only. You can toggle the **Show mismatches only** option to see all the articles you indicated for testing and what they each of them predicted as.

## Deploy your model

When you're satisfied with the training of your model, it's time to deploy it, which allows you to start classifying text through the API.

1. On the left panel, select **Deploying model**.
1. Select **Add deployment**, then enter `articles` in the **Create a new deployment name** field, and select **ClassifyArticles** in the **Model** field.
1. Select **Deploy** to deploy your model.
1. Once your model is deployed, leave that page open. You'll need your project and deployment name in the next step.

## Prepare to develop an app in Visual Studio Code

To test the text analytics capabilities of the Azure AI Language service, we'll use a simple PowerShell script in Visual Studio Code.

> **Tip**: If you have already cloned the **mslearn-ai-language** repo, open it in Visual Studio code. Otherwise, follow these steps to clone it to your development environment.

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a **Git: Clone** command to clone the `https://github.com/MicrosoftLearning/mslearn-ai-language` repository to a local folder (it doesn't matter which folder).
3. When the repository has been cloned, open the folder in Visual Studio Code.
4. Wait while additional files are installed to support the C# code projects in the repo.

    > **Note**: If you are prompted to add required assets to build and debug, select **Not Now**.

### Configure and run the PowerShell script

Now that you have a custom model, you can run a script that uses the Azure AI Language service.

1. In Visual Studio Code, in the **Explorer** pane, browse to the **Labfiles/04-text-classification** folder and open the classify-text.ps1 PowerShell script file.
1. Edit the top two lines of the script to replace the placeholders for **$key** and **$endpoint** with the key and endpoint got your Azure AI Language resource, and ensure that **$projectName**, and **$modelName** match what you entered above. Then save the changes to the file.
1. Right-click the **04-text-classification** folder and open an integrated terminal.

1. Run the following command to run the script and classify the **test1.txt** document. The script will only display the first few lines of the file and the predicted classification.

    ```powershell
    .\classify-text.ps1 test1.txt
    ```

    > **NOTE**
    > You can update the script variable `$verbose` to `$true` to see the raw response JSON.

1. Run the following command again, this time with a different file to classify:

    ```powershell
    .\classify-text.ps1 test2.txt
    ```

## Clean up

When you don't need your project anymore, you can delete if from your **Projects** page in Language Studio. You can also remove the Azure AI Language service and associated storage account in the [Azure portal](https://portal.azure.com).
