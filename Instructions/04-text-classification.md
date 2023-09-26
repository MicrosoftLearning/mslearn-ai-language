Azure AI Language provides several NLP capabilities, including the key phrase identification, text summarization, and sentiment analysis. The Language service also provides custom features like custom question answering and custom text classification.

To test the custom text classification of the Azure AI Language service, we'll configure the model using Language Studio then use a small command-line application that runs in the Cloud Shell to test it. The same pattern and functionality used here can be followed for real-world applications.

## Create an Azure AI Language service resource

To use custom text classification, you'll need to create an Azure AI Language service resource and select **Custom text classification & extraction** custom feature.

If you haven't already done so, create an **Azure AI Language service** resource in your Azure subscription.

1. In a browser, open the [Azure portal](https://portal.azure.com?azure-portal=true), and sign in with your Microsoft account.
1. Select the search field at the top of the portal, search for **Azure AI services**, and create a **Language Service** resource.
1. Select the box that includes **Custom text classification**. Then select **Continue to create your resource**.
1. Create a resource with the following settings:
    - **Subscription**: *Your Azure subscription*.
    - **Resource group**: *Select or create a resource group with a unique name*.
    - **Region**: *Choose any available region*:
    - **Name**: *Enter a unique name*.
    - **Pricing tier**: Standard S pricing tier
    - **Storage account**: New storage account
      - **Storage account name**: *Enter a unique name*.
      - **Storage account type**: Standard LRS
    - **Responsible AI notice**: Selected.

    >[!TIP]
    > You can reuse existing resources from previous labs if you have them available. Be sure to use a new container in the storage account to connect the custom entity extraction project to.

1. Select **Review + create,** then select **Create** to provision the resource.

### Get Language resource key and endpoint

1. Go to the resource group in the [Azure portal](https://portal.azure.com?azure-portal=true), and select the Azure AI Language resource.
1. Select **Keys and Endpoint** from the menu on the left side, located under **Resource Management**. You can copy it to your clipboard with the icon next to the key. We'll need one of the keys and the endpoint later, so either paste these values into Notepad for now or we'll come back to this page at that time.

## Upload sample articles

Once you've created the Azure AI Language service and storage account, you'll need to upload example articles to train your model later.

1. [Download sample articles](https://aka.ms/classification-articles) from this repository on GitHub. Extract the files in the `.zip` provided.

1. In the [Azure portal](https://portal.azure.com?azure-portal=true), navigate to the storage account you created, and select it

1. In your storage account, select **Containers** from the left menu, located below **Data storage**. On the screen that appears, select **+ Container**. Give the container the name `articles`, and set **Public access level** to **Container (anonymous read access for containers and blobs)**.

    > [!NOTE]
    > When you configure a storage account outside of this module, be careful to assign the appropriate access level. To learn more about each access level, see the [docs on Azure Storage](/azure/storage/blobs/anonymous-read-access-configure) .

1. After you've created the container, select it then select the **Upload** button. Select **Browse for files** to browse for the sample articles you downloaded. Then select **Upload**.

## Create a custom text classification project

After configuration is complete, create a custom text classification project. This project provides a working place to build, train, and deploy your model.

> [!NOTE]
> This lab utilizes **Language Studio**, but you can also create, build, train, and deploy your model through the REST API.

1. Sign into the [Language Studio](https://aka.ms/languageStudio) with your Azure account, and in the pane that appears, ensure the Azure subscription that you created your Azure AI Language resource in is selected. Make sure **Language** is selected for **Resource type** and select your Azure AI Language resource in the **Resource name** field. Then select **Done**.
1. Under the **Classify text** tab, select **Custom text classification**.
1. Select **+ Create new project**.
1. The **Connect storage** page appears. All values will already have been filled. So select **Next**.
1. On the **Select project type** page, select **Single label classification**. Then select **Next**.
1. On the **Enter basic information** pane, set the following:
    - Enter **ClassifyLab** for the **Name**.  
    - Set the **Text primary language** dropdown to **English (US)**.
    - Set the **Description** to **Custom text lab**.

1. Select **Next**.
1. On the **Choose container** page, set the **Blob store container** dropdown to your articles container.
1. Select the  **No, I need to label my files as part of this project** option. Then select **Next**.
1. Select **Create project**.

## Label your data

Now that your project is created, you need to label, or tag, your data to train your model how to classify text.

1. On the left, select **Data labeling**, if not already selected. You'll see a list of the files you uploaded to your storage account.
1. On the right side, in the **Activity** pane, select **+ Add class**.  The articles in this lab fall into four classes you'll need to create: **Classifieds**, **Sports**, **News**, and **Entertainment**.

    :::image type="content" source="../media/tag-data-add-class-new-small.png" alt-text="Screenshot showing the tag data page and the add class button."lightbox="../media/tag-data-add-class-new.png":::

1. After you've created your four classes, select **Article 1** to start. Here you can read the article, define which class this file is, and which dataset to assign it to.
1. Assign each article the appropriate class and dataset (training or testing) using the Activity pane on the right.  You can select a label from the list of lables on the right, and set each article to training or testing using the options at the bottom of the Activity pane. You  select **Next document** to move to the next document. For the purposes of this lab, we'll define which are to be used for training the model and testing the model:

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

    > [!NOTE]
    > Files in Language Studio are listed alphabetically, which is why the above list is not in sequential order. Make sure you visit both pages of documents when label your articles.

1. Select **Save labels** to save your labels.

## Train your model

Once you've labeled your data, you need to train your model.

1. Select **Training jobs** on the left side menu.
1. Select **Start a training job**.
1. Name your model **ClassifyArticles** under the **Train a new model** field.
1. Select **Use a manual split of training and testing data**.

    > [!TIP]
    > In your own classification projects, the Azure AI Language service will automatically split the testing set by percentage which is useful with a large dataset. With smaller datasets, it's important to train with the right class distribution.

1. Select **Train**

> [!IMPORTANT]
> Training your model can sometimes take several minutes. You'll get a notification when it's complete.

## Evaluate your model

In real world applications of text classification, it's important to evaluate and improve your model to verify it's performing as you expect.

1. Select **Model performance**, and select your **ClassifyArticles** model. There you can see the scoring of your model, performance metrics, and when it was trained. If the scoring of your model isn't 100%, it means that one of the documents used for testing didn't evaluate to what it was labeled. These failures can help you understand where to improve.
1. Select **Test set details** tab. If there are any errors, this tab allows you to see the articles you indicated for testing and what the model predicted them as and whether that conflicts with their test label. The tab defaults to show incorrect predictions only. You can toggle the **Show mismatches only** option to see all the articles you indicated for testing and what they each of them predicted as.

## Deploy your model

Once you're satisfied with the training of your model, it's time to deploy it, which allows you to start classifying text through the API.

1. On the left panel, select **Deploying model**.
1. Select **Add deployment**, then enter **articles** in the **Create a new deployment name** field, and select **ClassifyArticles** in the **Model** field.
1. Select **Deploy** to deploy your model.
1. Once your model is deployed, leave that page open. You'll need your project and deployment name in the next step.

## Send text classification to your model

To test the text analytics capabilities of the Azure AI Language service, we'll use a small command-line application that runs in the Cloud Shell on Azure.

### Run Cloud Shell

1. In the [Azure portal](https://portal.azure.com?azure-portal=true), select the **[>_]** (*Cloud Shell*) button at the top of the page to the right of the search box. This button opens a Cloud Shell pane at the bottom of the portal.

    :::image type="content" source="../media/powershell-portal-guide-1-small.png" alt-text="Screenshot of starting the Cloud Shell by clicking on the icon to the right of the top search box." lightbox="../media/powershell-portal-guide-1.png":::

1. The first time you open the Cloud Shell, you may be prompted to choose the type of shell you want to use (Bash or PowerShell). Select **PowerShell**. If you don't see this option, skip this step.  

1. If you're prompted to create storage for your Cloud Shell, ensure your subscription is specified and select **Create storage**. Then wait a minute or so for the storage to be created.

1. Make sure the type of shell indicated on the top left of the Cloud Shell pane is switched to **PowerShell**. If it's **Bash**, switch to **PowerShell** by using the dropdown menu on the top left of the shell.

1. Wait for PowerShell to start. You should see the following screen in the Azure portal:  

    :::image type="content" source="../media/powershell-prompt-small.png" alt-text="Screenshot of waiting for PowerShell to start." lightbox="../media/powershell-prompt.png":::

### Configure and run PowerShell

Now that you have a custom model, you can run a client application that uses the Azure AI Language service.

1. In the command shell, enter the following command to download the sample application and save it to a folder called **ai-language**. Press **Enter** to run the command:

    ```powershell
    git clone https://github.com/MicrosoftLearning/ai-language ai-language
    ```
  
    > [!TIP]
    > If you already used this command in another lab to clone the *ai-language* repository, you can skip this step.

1. The files are downloaded to a folder named **ai-language**. Now we want to see all of the files in your Cloud Shell storage and work with them. To navigate to the **Text Classification** folder, run the following command:

    ```powershell
    cd ai-language/text-classification
    ```

1. Type and run the following command into the shell:

    ```powershell
    code classify-text.ps1
    ```

1. In `classify-text.ps1`, note the top two lines of the script with places for your Azure AI Language service key and endpoint, as well as your project and model names. Replace the placeholders for **$key** and **$endpoint** with your resource values (**$projectName**, and **$modelName** should match what you entered above), and press **CTRL + S** to save the file.

    > [!TIP]
    > If you don't have these values readily available, navigate to the [Azure portal](https://portal.azure.com?azure-portal=true), find the Azure AI Language resource you created earlier, and select the **Keys and endpoint** page on the left.

1. Run the following command to call your model and classify the text provided. The script won't output the whole file it's classifying for the sake of space, but you can view the contents [here on GitHub](https://aka.ms/text-classification-repo). Review the output.

    ```powershell
    .\classify-text.ps1 test1.txt
    ```

    > [!NOTE]
    > You can update the script variable `$verbose` to `$true` to see the raw response JSON.

1. Run the following command again, this time with a different file to classify:

    ```powershell
    .\classify-text.ps1 test2.txt
    ```

1. Review the output.

## Clean up

When you don't need your project anymore, you can delete if from your **Projects** page in Language Studio. You can also remove the Azure AI Language service and associated storage account in the [Azure portal](https://portal.azure.com?azure-portal=true).
