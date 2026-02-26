# Requirements

## Run in Cloud Shell

* Azure subscription with OpenAI access
* If running in the Azure Cloud Shell, choose the Bash shell. The Azure CLI and Azure Developer CLI are included in the Cloud Shell.

## Run locally

* You can run the web app locally after running the deployment script:
    * [Azure Developer CLI (azd)](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd)
    * [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
    * Azure subscription with OpenAI access


## Environment Variables

The  `.env` file is created by the *azdeploy.sh* script. The AI model endpoint, API key, and model name are added during the deployment of the resources.

## Azure resource deployment

The provided `azdeploy.sh` creates the required resources in Azure:

* Change the two variables at the top of the script to match your needs, don't change anything else.
* The script:
    * Deploys the *gpt-4o* model using AZD.
    * Creates Azure Container Registry service
    * Uses ACR tasks to build and deploy the Dockerfile image to ACR
    * Creates the App Service Plan
    * Creates the App Service Web App
    * Configures the web app for container image in ACR
    * Configures the web app environment variables
    * The script will provide the App Service endpoint

The script provides two deployment options: 1. Full deployment; and 2. Redeploy the image only. Option 2 is only for post-deployment when you want to experiment with changes in the application. 

> Note: You can run the script in PowerShell, or Bash, using the `bash azdeploy.sh` command, this command also let's you run the script in Bash without having to make it an executable.

## Local development

### Provision AI model to Azure

You can run the run the project locally and only provision the AI model following these steps:

1. **Initialize environment** (choose a descriptive name):

   ```bash
   azd env new gpt-realtime-lab --confirm
   # or: azd env new your-name-gpt-experiment --confirm
   ```
   
   **Important**: This name becomes part of your Azure resource names!  
   The `--confirm` flag sets this as your default environment without prompting.

1. **Set your resource group**:

   ```bash
   azd env set AZURE_RESOURCE_GROUP "rg-your-name-gpt"
   ```

1. **Login and provision AI resources**:

   ```bash
   az login
   azd provision
   ```

    > **Important**: Do NOT run `azd deploy` - the app is not configured in the AZD templates.

If you only provisioned the model using the `azd provision` method you MUST create a `.env` file in the root of the directory with the following entries:

```
AZURE_VOICE_LIVE_ENDPOINT=""
AZURE_VOICE_LIVE_API_KEY=""
VOICE_LIVE_MODEL=""
VOICE_LIVE_VOICE="en-US-JennyNeural"
VOICE_LIVE_INSTRUCTIONS="You are a helpful AI assistant with a focus on world history. Respond naturally and conversationally. Keep your responses concise but engaging."
VOICE_LIVE_VERBOSE="" #Suppresses excessive logging to the terminal if running locally
```

Notes:

1. The endpoint is the endpoint for the model and it should only include `https://<proj-name>.cognitiveservices.azure.com`.
1. The API key is the key for the model.
1. The model is the model name used during deployment.
1. You can retrieve these values from the AI Foundry portal.

### Running the project locally

The project was was created and managed using **uv**, but it is not required to run. 

If you have **uv** installed:

* Run `uv venv` to create the environment
* Run `uv sync` to add packages
* Alias created for web app: `uv run web` to start the `flask_app.py` script.
* requirements.txt file created with `uv pip compile pyproject.toml -o requirements.txt`

If you don't have **uv** installed:

* Create environment: `python -m venv .venv`
* Activate environment: `.\.venv\Scripts\Activate.ps1`
* Install dependencies: `pip install -r requirements.txt`
* Run application (from project root): `python .\src\real_time_voice\flask_app.py`
