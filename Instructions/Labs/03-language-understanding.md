---
lab:
    title: 'Create a language understanding model with the Azure AI Language service'
    description: "Create a custom language understanding model to interpret input, predict intent, and identify entities."
---

# Create a language understanding model with the Language service

The Azure AI Language service enables you to define a *conversational language understanding* model that applications can use to interpret natural language *utterances* from users (text or spoken input),  predict the users *intent* (what they want to achieve), and identify any *entities* to which the intent should be applied.

For example, a conversational language model for a clock application might be expected to process input such as:

*What is the time in London?*

This kind of input is an example of an *utterance* (something a user might say or type), for which the desired *intent* is to get the time in a specific location (an *entity*); in this case, London.

> **NOTE**
> The task of a conversational language model is to predict the user's intent and identify any entities to which the intent applies. It is <u>not</u> the job of a conversational language model to actually perform the actions required to satisfy the intent. For example, a clock application can use a conversational language model to discern that the user wants to know the time in London; but the client application itself must then implement the logic to determine the correct time and present it to the user.

In this exercise, you'll use the Azure AI Language service to create a conversational language understand model, and use the Python SDK to implement a client app that uses it.

While this exercise is based on Python, you can develop conversational understanding applications using multiple language-specific SDKs; including:

- [Azure AI Conversations client library for Python](https://pypi.org/project/azure-ai-language-conversations/)
- [Azure AI Conversations client library for .NET](https://www.nuget.org/packages/Azure.AI.Language.Conversations)
- [Azure AI Conversations client library for JavaScript](https://www.npmjs.com/package/@azure/ai-language-conversations)

This exercise takes approximately **35** minutes.

## Provision an *Azure AI Language* resource

If you don't already have one in your subscription, you'll need to provision an **Azure AI Language service** resource in your Azure subscription.

1. Open the Azure portal at `https://portal.azure.com`, and sign in using the Microsoft account associated with your Azure subscription.
1. Select **Create a resource**.
1. In the search field, search for **Language service**. Then, in the results, select **Create** under **Language Service**.
1. Provision the resource using the following settings:
    - **Subscription**: *Your Azure subscription*.
    - **Resource group**: *Choose or create a resource group*.
    - **Region**: *Choose from one of the following regions*\*
        - Australia East
        - Central India
        - China East 2
        - East US
        - East US 2
        - North Europe
        - South Central US
        - Switzerland North
        - UK South
        - West Europe
        - West US 2
        - West US 3
    - **Name**: *Enter a unique name*.
    - **Pricing tier**: Select **F0** (*free*), or **S** (*standard*) if F is not available.
    - **Responsible AI Notice**: Agree.
1. Select **Review + create**, then select **Create** to provision the resource.
1. Wait for deployment to complete, and then go to the deployed resource.
1. View the **Keys and Endpoint** page. You will need the information on this page later in the exercise.

## Create a conversational language understanding project

Now that you have created an authoring resource, you can use it to create a conversational language understanding project.

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
    4. At the top of the page, click **Language Studio** to return to the Language Studio home page

1. At the top of the portal, in the **Create new** menu, select **Conversational language understanding**.

1. In the **Create a project** dialog box, on the **Enter basic information** page, enter the following details and then select **Next**:
    - **Name**: `Clock`
    - **Utterances primary language**: English
    - **Enable multiple languages in project?**: *Unselected*
    - **Description**: `Natural language clock`

1. On the **Review and finish** page, select **Create**.

### Create intents

The first thing we'll do in the new project is to define some intents. The model will ultimately predict which of these intents a user is requesting when submitting a natural language utterance.

> **Tip**: When working on your project, if some tips are displayed, read them and select **Got it** to dismiss them, or select **Skip all**.

1. On the **Schema definition** page, on the **Intents** tab, select **&#65291; Add** to add a new intent named `GetTime`.
1. Verify that the **GetTime** intent is listed (along with the default **None** intent). Then add the following additional intents:
    - `GetDay`
    - `GetDate`

### Label each intent with sample utterances

To help the model predict which intent a user is requesting, you must label each intent with some sample utterances.

1. In the pane on the left, select the **Data Labeling** page.

> **Tip**: You can expand the pane with the **>>** icon to see the page names, and hide it again with the **<<** icon.

1. Select the new **GetTime** intent  and enter the utterance `what is the time?`. This adds the utterance as sample input for the intent.
1. Add the following additional utterances for the **GetTime** intent:
    - `what's the time?`
    - `what time is it?`
    - `tell me the time`

    > **NOTE**
    > To add a new utterance, write the utterance in the textbox next to the intent and then press ENTER. 

1. Select the **GetDay** intent and add the following utterances as example input for that intent:
    - `what day is it?`
    - `what's the day?`
    - `what is the day today?`
    - `what day of the week is it?`

1. Select the **GetDate** intent and add the following utterances for it:
    - `what date is it?`
    - `what's the date?`
    - `what is the date today?`
    - `what's today's date?`

1. After you've added utterances for each of your intents, select **Save changes**.

### Train and test the model

Now that you've added some intents, let's train the language model and see if it can correctly predict them from user input.

1. In the pane on the left, select **Training jobs**. Then select **+ Start a training job**.

1. On the **Start a training job** dialog, select the option to train a new model, name it `Clock`. Select **Standard training** mode and the default **Data splitting** options.

1. To begin the process of training your model, select **Train**.

1. When training is complete (which may take several minutes) the job **Status** will change to **Training succeeded**.

1. Select the **Model performance** page, and then select the **Clock** model. Review the overall and per-intent evaluation metrics (*precision*, *recall*, and *F1 score*) and the *confusion matrix* generated by the evaluation that was performed when training (note that due to the small number of sample utterances, not all intents may be included in the results).

    > **NOTE**
    > To learn more about the evaluation metrics, refer to the [documentation](https://learn.microsoft.com/azure/ai-services/language-service/conversational-language-understanding/concepts/evaluation-metrics)

1. Go to the **Deploying a model** page, then select **Add deployment**.

1. On the **Add deployment** dialog, select **Create a new deployment name**, and then enter `production`.

1. Select the **Clock** model in the **Model** field then select **Deploy**. The deployment may take some time.

1. When the model has been deployed, select the **Testing deployments** page, then select the **production** deployment in the **Deployment name** field.

1. Enter the following text in the empty textbox, and then select **Run the test**:

    `what's the time now?`

    Review the result that is returned, noting that it includes the predicted intent (which should be **GetTime**) and a confidence score that indicates the probability the model calculated for the predicted intent. The JSON tab shows the comparative confidence for each potential intent (the one with the highest confidence score is the predicted intent)

1. Clear the text box, and then run another test with the following text:

    `tell me the time`

    Again, review the predicted intent and confidence score.

1. Try the following text:

    `what's the day today?`

    Hopefully the model predicts the **GetDay** intent.

## Add entities

So far you've defined some simple utterances that map to intents. Most real applications include more complex utterances from which specific data entities must be extracted to get more context for the intent.

### Add a learned entity

The most common kind of entity is a *learned* entity, in which the model learns to identify entity values based on examples.

1. In Language Studio, return to the **Schema definition** page and then on the **Entities** tab, select **&#65291; Add** to add a new entity.

1. In the **Add an entity** dialog box, enter the entity name `Location` and ensure that the **Learned** tab is selected. Then select **Add entity**.

1. After the **Location** entity has been created, return to the **Data labeling** page.
1. Select the **GetTime** intent and enter the following new example utterance:

    `what time is it in London?`

1. When the utterance has been added, select the word **London**, and in the drop-down list that appears, select **Location** to indicate that "London" is an example of a location.

1. Add another example utterance for the **GetTime** intent:

    `Tell me the time in Paris?`

1. When the utterance has been added, select the word **Paris**, and map it to the **Location** entity.

1. Add another example utterance for the **GetTime** intent:

    `what's the time in New York?`

1. When the utterance has been added, select the words **New York**, and map them to the **Location** entity.

1. Select **Save changes** to save the new utterances.

### Add a *list* entity

In some cases, valid values for an entity can be restricted to a list of specific terms and synonyms; which can help the app identify instances of the entity in utterances.

1. In Language Studio, return to the **Schema definition** page and then on the **Entities** tab, select **&#65291; Add** to add a new entity.

1. In the **Add an entity** dialog box, enter the entity name `Weekday` and select the **List** entity tab. Then select **Add entity**.

1. On the page for the **Weekday** entity, in the **Learned** section, ensure **Not required** is selected. Then, in the **List** section, select **&#65291; Add new list**. Then enter the following value and synonym and select **Save**:

    | List key | synonyms|
    |-------------------|---------|
    | `Sunday` | `Sun` |

    > **NOTE**
    > To enter the fields of the new list, insert the value `Sunday` in the text field, then click on the field where 'Type in value and press enter...' is displayed, enter the synonyms, and press ENTER.

1. Repeat the previous step to add the following list components:

    | Value | synonyms|
    |-------------------|---------|
    | `Monday` | `Mon` |
    | `Tuesday` | `Tue, Tues` |
    | `Wednesday` | `Wed, Weds` |
    | `Thursday` | `Thur, Thurs` |
    | `Friday` | `Fri` |
    | `Saturday` | `Sat` |

1. After adding and saving the list values, return to the **Data labeling** page.
1. Select the **GetDate** intent and enter the following new example utterance:

    `what date was it on Saturday?`

1. When the utterance has been added, select the word ***Saturday***, and in the drop-down list that appears, select **Weekday**.

1. Add another example utterance for the **GetDate** intent:

    `what date will it be on Friday?`

1. When the utterance has been added, map **Friday** to the **Weekday** entity.

1. Add another example utterance for the **GetDate** intent:

    `what will the date be on Thurs?`

1. When the utterance has been added, map **Thurs** to the **Weekday** entity.

1. select **Save changes** to save the new utterances.

### Add a *prebuilt* entity

The Azure AI Language service provides a set of *prebuilt* entities that are commonly used in conversational applications.

1. In Language Studio, return to the **Schema definition** page and then on the **Entities** tab, select **&#65291; Add** to add a new entity.

1. In the **Add an entity** dialog box, enter the entity name `Date` and select the **Prebuilt** entity tab. Then select **Add entity**.

1. On the page for the **Date** entity, in the **Learned** section, ensure **Not required** is selected. Then, in the **Prebuilt** section, select **&#65291; Add new prebuilt**.

1. In the **Select prebuilt** list, select **DateTime** and then select **Save**.
1. After adding the prebuilt entity, return to the **Data labeling** page
1. Select the **GetDay** intent and enter the following new example utterance:

    `what day was 01/01/1901?`

1. When the utterance has been added, select ***01/01/1901***, and in the drop-down list that appears, select **Date**.

1. Add another example utterance for the **GetDay** intent:

    `what day will it be on Dec 31st 2099?`

1. When the utterance has been added, map **Dec 31st 2099** to the **Date** entity.

1. Select **Save changes** to save the new utterances.

### Retrain the model

Now that you've modified the schema, you need to retrain and retest the model.

1. On the **Training jobs** page, select **Start a training job**.

1. On the **Start a training job** dialog,  select  **overwrite an existing model** and specify the **Clock** model. Select **Train** to train the model. If prompted, confirm you want to overwrite the existing model.

1. When training is complete the job **Status** will update to **Training succeeded**.

1. Select the **Model performance** page and then select the **Clock** model. Review the evaluation metrics (*precision*, *recall*, and *F1 score*) and the *confusion matrix* generated by the evaluation that was performed when training (note that due to the small number of sample utterances, not all intents may be included in the results).

1. On the **Deploying a model** page, select **Add deployment**.

1. On the **Add deployment** dialog, select **Override an existing deployment name**, and then select **production**.

1. Select the **Clock** model in the **Model** field and then select **Deploy** to deploy it. This may take some time.

1. When the model is deployed, on the **Testing deployments** page, select the **production** deployment under the **Deployment name** field, and then test it with the following text:

    `what's the time in Edinburgh?`

1. Review the result that is returned, which should hopefully predict the **GetTime** intent and a **Location** entity with the text value "Edinburgh".

1. Try testing the following utterances:

    `what time is it in Tokyo?`

    `what date is it on Friday?`

    `what's the date on Weds?`

    `what day was 01/01/2020?`

    `what day will Mar 7th 2030 be?`

## Use the model from a client app

In a real project, you'd iteratively refine intents and entities, retrain, and retest until you are satisfied with the predictive performance. Then, when you've tested it and are satisfied with its predictive performance, you can use it in a client app by calling its REST interface or a runtime-specific SDK.

### Prepare to develop an app in Cloud Shell

You'll develop your language understanding app using Cloud Shell in the Azure portal. The code files for your app have been provided in a GitHub repo.

1. In the Azure Portal, use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    **<font color="red">Ensure you've switched to the classic version of the cloud shell before continuing.</font>**

1. In the PowerShell pane, enter the following commands to clone the GitHub repo for this exercise:

    ```
   rm -r mslearn-ai-language -f
   git clone https://github.com/microsoftlearning/mslearn-ai-language
    ```

    > **Tip**: As you paste commands into the cloudshell, the ouput may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. After the repo has been cloned, navigate to the folder containing the application code files:  

    ```
   cd mslearn-ai-language/Labfiles/03-language/Python/clock-client
    ```

### Configure your application

1. In the command line pane, run the following command to view the code files in the **clock-client** folder:

    ```
   ls -a -l
    ```

    The files include a configuration file (**.env**) and a code file (**clock-client.py**).

1. Create a Python virtual environment and install the Azure AI Language Conversations SDK package and other required packages by running the following command:

    ```
   python -m venv labenv
    ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-language-conversations==1.1.0
    ```
1. Enter the following command to edit the configuration file:

    ```
   code .env
    ```

    The file is opened in a code editor.

1. Update the configuration values to include the  **endpoint** and a **key** from the Azure Language resource you created (available on the **Keys and Endpoint** page for your Azure AI Language resource in the Azure portal).
1. After you've replaced the placeholders, within the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

### Add code to the application

1. Enter the following command to edit the application code file:

    ```
   code clock-client.py
    ```

1. Review the existing code. You will add code to work with the AI Language Conversations SDK.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces** and add the following code to import the namespaces you will need to use the AI Language Conversations SDK:

    ```python
   # Import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.language.conversations import ConversationAnalysisClient
    ```

1. In the **main** function, note that code to load the prediction endpoint and key from the configuration file has already been provided. Then find the comment **Create a client for the Language service model** and add the following code to create a conversation analysis client for your AI Language service:

    ```python
   # Create a client for the Language service model
   client = ConversationAnalysisClient(
        ls_prediction_endpoint, AzureKeyCredential(ls_prediction_key))
    ```

1. Note that the code in the **main** function prompts for user input until the user enters "quit". Within this loop, find the comment **Call the Language service model to get intent and entities** and add the following code:

    ```python
   # Call the Language service model to get intent and entities
   cls_project = 'Clock'
   deployment_slot = 'production'

   with client:
        query = userText
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": query
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": cls_project,
                    "deploymentName": deployment_slot,
                    "verbose": True
                }
            }
        )

   top_intent = result["result"]["prediction"]["topIntent"]
   entities = result["result"]["prediction"]["entities"]

   print("view top intent:")
   print("\ttop intent: {}".format(result["result"]["prediction"]["topIntent"]))
   print("\tcategory: {}".format(result["result"]["prediction"]["intents"][0]["category"]))
   print("\tconfidence score: {}\n".format(result["result"]["prediction"]["intents"][0]["confidenceScore"]))

   print("view entities:")
   for entity in entities:
        print("\tcategory: {}".format(entity["category"]))
        print("\ttext: {}".format(entity["text"]))
        print("\tconfidence score: {}".format(entity["confidenceScore"]))

   print("query: {}".format(result["result"]["query"]))
    ```

    The call to the conversational understanding model returns a prediction/result, which includes the top (most likely) intent as well as any entities that were detected in the input utterance. Your client application must now use that prediction to determine and perform the appropriate action.

1. Find the comment **Apply the appropriate action**, and add the following code, which checks for intents supported by the application (**GetTime**, **GetDate**, and **GetDay**) and determines if any relevant entities have been detected, before calling an existing function to produce an appropriate response.

    ```python
   # Apply the appropriate action
   if top_intent == 'GetTime':
        location = 'local'
        # Check for entities
        if len(entities) > 0:
            # Check for a location entity
            for entity in entities:
                if 'Location' == entity["category"]:
                    # ML entities are strings, get the first one
                    location = entity["text"]
        # Get the time for the specified location
        print(GetTime(location))

   elif top_intent == 'GetDay':
        date_string = date.today().strftime("%m/%d/%Y")
        # Check for entities
        if len(entities) > 0:
            # Check for a Date entity
            for entity in entities:
                if 'Date' == entity["category"]:
                    # Regex entities are strings, get the first one
                    date_string = entity["text"]
        # Get the day for the specified date
        print(GetDay(date_string))

   elif top_intent == 'GetDate':
        day = 'today'
        # Check for entities
        if len(entities) > 0:
            # Check for a Weekday entity
            for entity in entities:
                if 'Weekday' == entity["category"]:
                # List entities are lists
                    day = entity["text"]
        # Get the date for the specified day
        print(GetDate(day))

   else:
        # Some other intent (for example, "None") was predicted
        print('Try asking me for the time, the day, or the date.')
    ```

1. Save your changes (CTRL+S), then enter the following command to run the program (you maximize the cloud shell pane and resize the panels to see more text in the command line pane):

    ```
   python clock-client.py
    ```

1. When prompted, enter utterances to test the application. For example, try:

    *Hello*

    *What time is it?*

    *What's the time in London?*

    *What's the date?*

    *What date is Sunday?*

    *What day is it?*

    *What day is 01/01/2025?*

    > **Note**: The logic in the application is deliberately simple, and has a number of limitations. For example, when getting the time, only a restricted set of cities is supported and daylight savings time is ignored. The goal is to see an example of a typical pattern for using Language Service in which your application must:
    >   1. Connect to a prediction endpoint.
    >   2. Submit an utterance to get a prediction.
    >   3. Implement logic to respond appropriately to the predicted intent and entities.

1. When you have finished testing, enter *quit*.

## Clean up resources

If you're finished exploring the Azure AI Language service, you can delete the resources you created in this exercise. Here's how:

1. Close the Azure cloud shell pane
1. In the Azure portal, browse to the Azure AI Language resource you created in this lab.
1. On the resource page, select **Delete** and follow the instructions to delete the resource.

## More information

To learn more about conversational language understanding in  Azure AI Language, see the [Azure AI Language documentation](https://learn.microsoft.com/azure/ai-services/language-service/conversational-language-understanding/overview).
