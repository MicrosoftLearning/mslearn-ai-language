---
lab:
  title: Develop a text analysis agent
  description: Use Azure Language in Foundry Tools to add text analysis capabilities
    to an AI agent.
  duration: 30
  level: 300
  islab: true
  primarytopics:
  - Azure
  - Azure Language
---

# Develop a text analysis agent

**Azure Language in Foundry Tools** supports analysis of text, including language detection, sentiment analysis, key phrase extraction, entity recognition, and summarization.

You can use the service directly in an application through its REST API and several language-specific SDKs. You can also use the **Azure Language in Foundry Tools MCP server** to integrate its capabilities into an AI agent; which is what you'll do in this exercise.

> **Tip**: The code used in this exercise is based on the for Microsoft Foundry SDK for Python. You can develop similar solutions using the SDKs for Microsoft .NET, JavaScript, and Java. Refer to [Microsoft Foundry SDK client libraries](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) for details.

This exercise takes approximately **30** minutes.

## Prerequisites

Before starting this exercise, ensure you have:

- An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account)
- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Python version 3.13 or higher](https://www.python.org/downloads/) installed
- [Git](https://git-scm.com/install/) installed and configured

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the Foundry logo at the top left to navigate to the home page.

1. If it is not already enabled, in the tool bar the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name; expanding the **Advanced options** area to specify the following settings for your project:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select any of the **AI Foundry recommended** regions

    > **TIP**: Remember (or make a note of) the Foundry resource name - you're going to need it later!

1. Select **Create**. Wait for your project to be created.
1. On the home page for your project, note the project endpoint, key, and OpenAI endpoint.

    > **TIP**: Copy the project key to the clipboard - you're going to need it later!

## Create an agent

Now that you have a Foundry project, you can create an agent.

1. In the **Start building** menu, select **Create agent**; and when prompted, name the agent `Text-Analysis-Agent`.

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

    The agent should open in the playground, with the Azure Language in Foundry Tools tool connected.

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

## Create a client application

Now that you have a working agent, you can create a client application that uses it.

### Get the application files from GitHub

1. Open Visual Studio Code.
1. Open the command palette (*Ctrl+Shift+P*) and use the `Git:clone` command to clone the `https://github.com/microsoftlearning/mslearn-ai-language` repo to a local folder (it doesn't matter which one). Then open it.

    You may be prompted to confirm you trust the authors.

1. After the repo has been cloned, in the Explorer pane, navigate to the folder containing the application code files at **/Labfiles/02-language-agent/Python/text-agent**. The application files include:
    - **.env** (the application configuration file)
    - **requirements.txt** (the Python package dependencies that need to be installed)
    - **text-agent.py** (the code file for the application)

### Configure the application

1. In Visual Studio Code, view the **Extensions** pane; and if it is not already installed, install the **Python** extension.
1. In the **Command Palette**, use the command `python:select interpreter`. Then select an existing environment if you have one, or create a new **Venv** environment based on your Python 3.1x installation.

    > **Tip**: If you are prompted to install dependencies, you can install the ones in the *requirements.txt* file in the */Labfiles/02-language-agent/Python/text-agent* folder; but it's OK if you - don't we'll install them later!

1. In the **Explorer** pane, right-click the **text-agent** folder containing the application files, and select **Open in integrated terminal** (or open a terminal in the **Terminal** menu and navigate to the */Labfiles/02-language-agent/Python/text-agent* folder.)

    > **Note**: Opening the terminal in Visual Studio Code will automatically activate the Python environment. You may need to enable running scripts on your system.

1. Ensure that the terminal is open in the **text-agent** folder with the prefix **(.venv)** to indicate that the Python environment you created is active.
1. Install the Foundry SDK package, the Azure Identity package, and other required packages by running the following command:

    ```
    pip install -r requirements.txt azure-identity --pre azure-ai-projects==2.0.0b4
    ```

1. In the **Explorer** pane, in the **text-agent** folder, select the **.env** file to open it. Then update the configuration values to include your project **endpoint** (from the project home page in Foundry Portal) and the name of your agent (which should be **Text-Analysis-Agent** - note that this name is case-sensitive).
1. Save the modified configuration file.

### Implement application code

1. In the **Explorer** pane, in the **text-agent** folder,  open the **text-agent.py** file.
1. Review the existing code. You will add code to submit prompts to your agent.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces** and add the following code to import the namespaces you will need:

    ```python
   # import namespaces
   from azure.identity import DefaultAzureCredential
   from azure.ai.projects import AIProjectClient
    ```

1. In the **main** function, note that code to load the endpoint and key from the configuration file has already been provided. Then find the comment **Get project client**, and add the following code to create a client for your Foundry project:

    ```python
   # Get project client
   project_client = AIProjectClient(
        endpoint=foundry_endpoint,
        credential=DefaultAzureCredential(),
   )
    ```

1. Find the comment **Get an OpenAI client**, and add the following code to get an OpenAI client with which to call your agent.

    ```python
   # Get an OpenAI client
   openai_client = project_client.get_openai_client()
    ```

1. Find the comment **Use the agent to get a response**, and add the following code to submit a user prompt to your agent, and display the response.

    ```python
   # Use the agent to get a response
   prompt = input("User prompt: ")
   response = openai_client.responses.create(
        input=[{"role": "user", "content": prompt}],
        extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
   )

   print(f"{agent_name}: {response.output_text}")
    ```

1. Save the changes you made to the code file.

## Test the client application

Now let's test the application by running it in a Python environment and authenticating the connection to your project.

1. In the Visual Studio Code terminal, enter the following command to sign into Azure

   ```powershell
    az login
    ```

    When prompted, sign into Azure using your credentials.

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See *[Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively)* for details.

1. In the Visual Studio Code terminal, confirm the details of your Azure subscription; and then enter the following command to run the client application:

    ```powershell
    python text-agent.py
    ```

1. When prompted, enter the following prompt:

    ```
    Extract named entities from the following text: "Pierre and I went to Paris on July 14th."
    ```

1. Review the response, which should identify named people, places, and dates.

## View tool details

The Azure Language in Foundry Tools tool provides a wide range of functionality, and the agent must select the appropriate function to call. We can see the options available in the agent's response.

1. In the **text-agent.py** code file, add the following line immediately after the *print(f"{agent_name}: {response.output_text}")* line you added previously (before the *except Exception as ex:* line):

    ```python
    print(f"\nResponse Details: {response.model_dump_json(indent=2)}")
    ```

1. Save the changes to the code file.
1. In the terminal, re-enter the command to run the application (`python text-agent.py`).
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
