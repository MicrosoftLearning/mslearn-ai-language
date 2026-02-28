---
lab:
    title: 'Develop a text analysis agent'
    description: 'Use Azure Language in Foundry Tools to add text analysis capabilities to an AI agent.'
    duration: 30
    level: 300
---

# Develop a text analysis agent

**Azure Language in Foundry Tools** supports analysis of text, including language detection, sentiment analysis, key phrase extraction, entity recognition, and summarization.

You can use the service directly in an application through its REST API and several language-specific SDKs. You can also use the **Azure Language in Foundry Tools MCP server** to integrate its capabilities into an AI agent; which is what you'll do in this exercise.

This exercise takes approximately **30** minutes.

## Prerequisites

Before starting this exercise, ensure you have:
- Visual Studio Code installed
- An active Azure subscription
- Python version 3.10 or higher installed

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open Microsoft Foundry at https://ai.azure.com and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the Foundry logo at the top left to navigate to the home page.

1. If it is not already enabled, in the tool bar the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name; expanding the **Advanced options** area to specify the following settings for your project:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select any of the **AI Foundry recommended** regions

    > **TIP**: Remember the resource name - you're going to need it later!

1. Select **Create**. Wait for your project to be created.
1. On the home page for your project, note the project endpoint, key, and region.

    > **TIP**: Copy the project key to the clipboard - you're going to need it later!

## Create an agent

Now that you have a Foundry project, you can create an agent.

1. In the **Start building** menu, select **Create agent**; and when prompted, name the agent **Text-Analysis-Agent**.

    When ready, your agent opens in the agent playground.

1. In the model drop-down list, ensure that a **gpt-4.1** model has been deployed and selected for your agent.
1. Assign your agent the following **Instructions**:

    ```
   You are an AI agent that assists users by helping them analyze and summarize text.
    ```

1. Use the **Save** button to save the changes.
1. Test the agent by entering the following prompt in the **Chat** pane:

    ```
   What can you help me with?
    ```

    The agent should respond with an appropriate answer based on its instructions.

## Create an Azure Language in Foundry Tools connection

Foundry includes an MCP server for Azure Language in Foundry Tools, which you can connect to your project and use in your agent.

1. In the navigation pane on the left, select the **Tools** page.
1. Connect a tool; selecting **Azure Language in Foundry Tools** in the **Catalog** and specifying the following configuration
    - **Foundry resource name**: *Enter the name of your Foundry resource (for example, `{project_name}-resource)`*
    - **Authentication**: Key-based
    - **Credential** (**Ocp-Apim-Subscription-Key**): *enter (or paste) the key for your Foundry project*

1. Wait for the MCP tool connection to be created, and then view its details page.
1. On the details page for the Azure Language in Foundry Tools connection, select **Use in an agent**, and then select the **Text-Analysis-Agent** agent you created previously.

    The agent should open in te playground, with the Azure Language in Foundry Tools tool connected.

## Test the Azure Language tool in the playground

Now let's test the agent's ability to use the tool you connected.

1. In the agent playground for the **Text-Analysis-Agent** agent, modify the instructions as follows:

    ```
   You are an AI agent that assists users by helping them analyze and summarize text. Use the Azure Language tool to perform text analysis tasks.
    ```
1. Use the **Save** button to save the changes.
1. Test the agent by entering the following prompt in the **Chat** pane:

    ```
    Summarize this article, and use named entity recognition to identify people, places, and dates:

    Microsoft was founded on April 4, 1975, by childhood friends Bill Gates (then 19) and Paul Allen (22) after they were inspired by the Altair 8800, one of the first personal computers, featured on the cover of *Popular Electronics*. They contacted the Altair’s maker, MITS, and successfully developed a version of the BASIC programming language, despite initially not owning the machine themselves. The pair formed a partnership called “Micro‑Soft” in Albuquerque, New Mexico, close to MITS’s headquarters, with the goal of writing software for emerging microcomputers.

    In the late 1970s, Microsoft grew by supplying programming languages to multiple hardware vendors, then relocated to the Seattle area in 1979. A pivotal moment came in 1980 when Microsoft partnered with IBM to provide an operating system for the IBM PC, leading to MS‑DOS and establishing the company’s dominance in personal computing. Gates guided the company’s long-term strategy as CEO, while Allen contributed key technical vision in its early years, setting Microsoft on a path that would reshape the software industry.
    ```

1. When prompted, approve use of the Azure Language tool by selecting **Always approve all Azure Language in Foundry Tools tools** (you may need to do this twice because the prompt asked for two distinct text analysis tasks).
1. Review the response, which should summarize the article about the founding of Microsoft and list the key people, places, and dates it mentions.
1. Review the **Logs** for the chat and verify that the Azure Language tool was used by the agent to process the prompt.
1. In the pane on the left, in the menu for the Azure Language in Foundry Tools tool (**&#8942;**), select **Configure** and verify that the **Require approval before using tool** setting is **Always approval all tools**. If not, change the setting and add the configuration, and then save the agent. 

## Create a client application

Now that you have a working agent, you can create a client application that uses it.

1. In the agent playground, select the **Code** tab to view sample code for your agent; then view the **Python** sample code. You'll use this as the starting point for your client application.
1. Keeping the Microsoft Foundry playground page open in the browser, open Visual Studio Code.
1. In Visual Studio Code, select the option to open a folder (or on the **File** menu, select **Open folder**), and when prompted, create a new empty folder named **Text-Client** (it doesn't matter where) and open it. If prompted, confirm that you trust the creator of the folder.
1. Create a new file named **.env** in the **Text-Client** folder - you'll use this file for environment variables used in your Python code.
1. Create a second file named **app.py** in the **Text-Client** folder - you'll use this file for your Python application code.

    **TIP**: If you are prompted to install the Visual Studio Code extension for Python, you can do so; but it's not required for this exercise.

1. Return to the Foundry playground, and in the **Code** pane for the **Text-Analysis-Agent** agent, select the **{x}** icon to view the environment variables for your agent, and copy them to the clipboard.
1. In Visual Studio Code, paste the copied environment variables into the **.env** file and save it.
1. Return to the Foundry playground, and in the **Code** pane for the **Text-Analysis-Agent** agent, copy the Python sample code to the clipboard.
1. In Visual Studio Code, paste the copied code into the **app.py** file.
1. In the code you pasted, find the comment **# Reference the agent to get a response**, and modify the code under this comment as follows:

    ```python
    # Reference the agent to get a response
    prompt = input("Enter a prompt to send to the agent: ")
    response = openai_client.responses.create(
        input=[{"role": "user", "content": prompt}],
        extra_body={"agent_reference": {"name": myAgent, "version": myVersion, "type": "agent_reference"}},)
    
    print(f"Response output: {response.output_text}")
    ```

1. Save the changes you made to the code file.

## Test the client application

Now let's test the application by running it in a Python environment and authenticating the connection to your project.

1. In the **View** menu, select **Command Palette** and enter the comment `python:select interpreter`. Then create a new **Venv** environment based on your Python 3.1x installation.
1. In the Visual Studio Code **View** menu, select **Terminal** to open a terminal pane. Ensure that the terminal is open in the **Text-Client** folder with the prefix **(.venv)** to indicate that the Python environment you created is active.
1. View the **pip install ...** statements in the comments at the top of the **app.py** code file. These commands install the required Python packages to use the Foundry SDK to call your agent. Enter each of these commands in the terminal to install the required packages.
1. When the packages have been installed, enter the following command to sign into Azure

   ```powershell
    az login
    ```

    When prompted, sign into Azure using your credentials.

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See *[Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively)* for details.

1. In the Visual Studio Code terminal, view the details of your Azure subscription; and then enter the following command to run the client application:

    ```powershell
    python app.py
    ```

1. When prompted, enter the following prompt:

    ```
    Extract named entities from the following text: "Pierre and I went to Paris on July 14th."
    ```
1. Review the response, which should identify named people, places, and dates.

## View tool details

The Azure Language in Foundry Tools tool provides a wide range of functionality, and the agent must select the appropriate function to call. We can see the options available in the agent's response.

1. In the app.py code file, add the following line to the end of the current code:

    ```python
    print(f"\nResponse Details: {response.model_dump_json(indent=2)}")
    ```

1. Save the changes to the code file.
1. In the terminal, re-enter the command to run the application (`python app.py`).
1. When prompted, enter the following command:

    ```
    Tell me what entities and dates are mentioned in this review, and whether it is positive or negative: "I booked my flight to Paris in July with Margie's Travel, and it was fantastic!"
    ```

1. Review the response (you may need to scroll quite far up to see it), which should identify entities and dates, and determine the sentiment of the text.
1. Review the JSON response details, which indicate each of the tools available to the agent. In this case, it should have used the **extract_named_entities_from_text** and **detect_sentiment_from_text** tools within Azure Language in Foundry Tools.

## Clean up resources

If you're finished exploring the Azure AI Language service, you can delete the resources you created in this exercise. Here's how:

1. In the Azure portal, browse to the Foundry resource you created in this lab.
1. On the resource page, select **Delete** and follow the instructions to delete the resource.
