#!/usr/bin/env bash

# Script to deploy the Flask app to Azure App Service using a container from ACR
# and provision AI Foundry with gtp-realtime model using AZD.

# Only change the rg (resource group) and location variables below if needed.

rg="rg-voicelive" # Replace with your resource group
location="eastus2" # Or a location near you


# ============================================================================
# DON'T CHANGE ANYTHING BELOW THIS LINE.
# ============================================================================


# ============================================================================
# Deployment Mode Selection
# ============================================================================
clear
echo "Select deployment mode:"
echo "  1) Full deployment (AI Foundry + Container + App Service) - ~15 minutes"
echo "  2) Container update only (requires full deployment first) - ~5 minutes"
echo ""
read -p "Enter choice (1 or 2): " deploy_mode

if [ "$deploy_mode" != "1" ] && [ "$deploy_mode" != "2" ]; then
    echo "ERROR: Invalid choice. Please enter 1 or 2."
    exit 1
fi

# ============================================================================
# Service Name Generation (shared by both modes)
# ============================================================================
# Generate consistent unique hash from Azure user object ID (guaranteed unique per user)
user_object_id=$(az ad signed-in-user show --query "id" -o tsv 2>/dev/null)
if [ -z "$user_object_id" ]; then
    echo "ERROR: Not authenticated with Azure. Please run: az login"
    exit 1
fi
user_hash=$(echo -n "$user_object_id" | sha1sum | cut -c1-8)

# Build ACR name: 'acr' prefix + 8-char hash (no hyphens, all lowercase, starts with letter)
acr_name="acr${user_hash}"

# App Service plan and webapp (hyphens allowed)
appsvc_plan="appplan-${user_hash}"
webapp_name="webapp-${user_hash}"
image="rt-voice"
tag="v1"
azd_env_name="gpt-realtime" # Forced as unique at each run

# ============================================================================
# Mode 2: Container Update Only
# ============================================================================
if [ "$deploy_mode" = "2" ]; then
    clear
    echo "Starting container update (rebuild + redeploy)..."
    echo ""

    # Verify that the resources exist
    echo "  - Verifying existing resources..."
    if ! az acr show -n $acr_name -g $rg >/dev/null 2>&1; then
        echo "ERROR: ACR '$acr_name' not found in resource group '$rg'"
        echo "You must run a full deployment (option 1) first."
        exit 1
    fi

    if ! az webapp show -n $webapp_name -g $rg >/dev/null 2>&1; then
        echo "ERROR: Web App '$webapp_name' not found in resource group '$rg'"
        echo "You must run a full deployment (option 1) first."
        exit 1
    fi

    echo "  - Resources verified: ACR and Web App exist"

    # Build image
    echo "  - Building updated image in ACR...(takes 3-5 minutes)"
    max_retries=3
    retry_count=0

    while [ "${retry_count}" -lt "${max_retries}" ]; do
        echo "  - Attempt $((retry_count + 1)) of $max_retries: building image..."

        az acr build -r $acr_name --image ${acr_name}.azurecr.io/${image}:${tag} --file Dockerfile . >/dev/null 2>&1

        if az acr repository show --name $acr_name --repository $image >/dev/null 2>&1; then
            echo "  - Image successfully built and verified in ACR"
            break
        else
            echo "  - Image not found in ACR, retrying build..."
            retry_count=$((retry_count + 1))
            if [ $retry_count -lt $max_retries ]; then
                echo "  - Waiting 5 seconds before retry..."
                sleep 5
            fi
        fi
    done

    if [ $retry_count -eq $max_retries ]; then
        echo "ERROR: Failed to build image after $max_retries attempts"
        exit 1
    fi

    # Restart web app to pull new image
    echo "  - Restarting Web App to pull updated container..."
    az webapp restart --name "$webapp_name" --resource-group "$rg" >/dev/null

    echo ""
    echo "Container update complete!"
    echo " - Your app is available at: https://${webapp_name}.azurewebsites.net"
    echo " - App may take 1-2 minutes to restart with the new image."
    echo ""
    exit 0
fi

# ============================================================================
# Mode 1: Full Deployment (original script flow)
# ============================================================================

# Create the .env file
cat > .env << 'EOF'
# Do not change any settings in this file. Endpoint, API key, and model name are set automatically during deployment
AZURE_VOICE_LIVE_ENDPOINT=""
AZURE_VOICE_LIVE_API_KEY=""
VOICE_LIVE_MODEL=""
VOICE_LIVE_VOICE="en-US-JennyNeural"
VOICE_LIVE_INSTRUCTIONS="You are a helpful AI assistant with a focus on world history. Respond naturally and conversationally. Keep your responses concise but engaging."
VOICE_LIVE_VERBOSE="" #Suppresses excessive logging to the terminal if running locally
EOF

clear
echo "Starting FULL deployment with AZD provisioning + App Service, takes about 15 minutes..."

# Step 1: Provision AI Foundry with GPT Realtime model using AZD
echo
echo "Step 1: Provisioning AI Foundry with GPT Realtime model..."
echo "  - Setting up AZD environment..."
# Clear local azd state only (safe for students - doesn't delete Azure resources)
rm -rf ~/.azd 2>/dev/null || true
# Also clear any project-level azd state
rm -rf .azure 2>/dev/null || true

# Create fresh environment with unique name
timeout 5 azd env new $azd_env_name --confirm >/dev/null 2>&1 || azd env new $azd_env_name >/dev/null 2>&1
azd env set AZURE_LOCATION $location >/dev/null
azd env set AZURE_RESOURCE_GROUP $rg >/dev/null
subscription_id=$(az account show --query id -o tsv)
azd env set AZURE_SUBSCRIPTION_ID "$subscription_id" >/dev/null
echo "  - AZD environment '$azd_env_name' created (fresh state)"

echo "  - Provisioning AI resources (forcing new deployment)..."
echo "  - Authenticating azd with Azure..."
# Try ambient auth (Cloud Shell) with a 10s timeout to avoid hanging.
# If it doesn't complete quickly, fall back to interactive device code.
if ! timeout 5 azd auth login >/dev/null 2>&1; then
    azd auth login --use-device-code
fi

# Force a completely fresh deployment by combining multiple techniques
azd config set alpha.infrastructure.deployment.name "azd-gpt-realtime-$(date +%s)"
# Clear any cached deployment state and force deployment
azd env refresh --no-prompt 2>/dev/null || true

# Provision with retry logic to handle non-terminal resource state conflicts
provision_retries=3
provision_attempt=0
while [ $provision_attempt -lt $provision_retries ]; do
    provision_attempt=$((provision_attempt + 1))
    echo "  - Running azd provision (attempt $provision_attempt of $provision_retries)..."
    if azd provision; then
        break
    fi
    if [ $provision_attempt -lt $provision_retries ]; then
        echo "  - Provision failed (possible non-terminal resource conflict). Waiting 60 seconds before retry..."
        sleep 60
    else
        echo "ERROR: azd provision failed after $provision_retries attempts."
        exit 1
    fi
done

echo "  - Retrieving AI Foundry endpoint, API key, and model name..."
endpoint=$(azd env get-values --output json | jq -r '.AZURE_OPENAI_ENDPOINT')
api_key=$(azd env get-values --output json | jq -r '.AZURE_OPENAI_API_KEY')
model_name=$(azd env get-values --output json | jq -r '.AZURE_OPENAI_REALTIME_MODEL_NAME')

if [ "$endpoint" = "null" ] || [ "$endpoint" = "" ] || [ "$api_key" = "null" ] || [ "$api_key" = "" ] || [ "$model_name" = "null" ] || [ "$model_name" = "" ]; then
    echo "ERROR: Failed to retrieve AI Foundry endpoint, API key, or model name from azd"
    echo "Please check the azd provision output and try again"
    exit 1
fi

echo "  - Updating .env file with AI Foundry credentials..."
# Update .env file with the retrieved values
if [ -f .env ]; then
    # Use sed to update existing values or add them if they don't exist
    sed -i "s|^AZURE_VOICE_LIVE_ENDPOINT=.*|AZURE_VOICE_LIVE_ENDPOINT=\"$endpoint\"|" .env
    sed -i "s|^AZURE_VOICE_LIVE_API_KEY=.*|AZURE_VOICE_LIVE_API_KEY=\"$api_key\"|" .env
    sed -i "s|^VOICE_LIVE_MODEL=.*|VOICE_LIVE_MODEL=\"$model_name\"|" .env
    echo "  - .env file updated with AI Foundry credentials and model name"
else
    echo "ERROR: .env file not found"
    exit 1
fi

echo "  - AI Foundry provisioning complete!"

# Step 2: Continue with App Service deployment
echo
echo "Step 2: Create ACR and App Service resources..."

# Create ACR and build image from Dockerfile
echo "  - Creating Azure Container Registry resource..."
az acr create -n $acr_name -g $rg --sku Basic --admin-enabled true >/dev/null
echo "  - Resource created"
echo "  - Starting image build process in 10 seconds to reduce build failures."
sleep 10 # To give time for the ACR service to be ready for build operations
echo "  - Building image in ACR...(takes 3-5 minutes per attempt)"
# Build image with retry logic
max_retries=3
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    echo "  - Attempt $((retry_count + 1)) of $max_retries: building image..."

    # Run the build command
    az acr build -r $acr_name --image ${acr_name}.azurecr.io/${image}:${tag} --file Dockerfile . >/dev/null 2>&1

    # Check if the image exists in the registry
    if az acr repository show --name $acr_name --repository $image >/dev/null 2>&1; then
        echo "  - Image successfully built and verified in ACR..."
        break
    else
        echo "  - Image not found in ACR, retrying build..."
        retry_count=$((retry_count + 1))
    if [ "${retry_count}" -lt "${max_retries}" ]; then
            echo "  - Waiting 5 seconds before retry..."
            sleep 5
        fi
    fi
done


if [ "${retry_count}" -eq "${max_retries}" ]; then
    echo "ERROR: Failed to build image after $max_retries attempts"
    echo "Please check your Dockerfile and try again manually with:"
    echo "az acr build -r $acr_name --image ${acr_name}.azurecr.io/${image}:${tag} --file Dockerfile ."
    exit 1
fi

echo "  - Container image build complete!"

echo
echo "Step 3: Configuring Azure App Service with updated credentials..."

echo "  - Gathering environment variables from .env file for App Service deployment.."
# Parse the .env file exists in the repo root, and bring values into the  script environment
if [ -f .env ]; then
    while IFS='=' read -r key val; do
        # Trim whitespace
        key=$(echo "$key" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        # Skip comments and empty lines
        case "$key" in
            ""|\#*) continue;;
        esac
        # Join remainder of line in case value contains '='
        if echo "$val" | grep -q "="; then
            # Re-read the whole line and extract first = split only
            val=$(echo "${key}=${val}" | sed 's/^[^=]*=//')
        fi
        val=$(echo "$val" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        # Remove surrounding quotes if present
        val="${val%\"}"
        val="${val#\"}"
        val="${val%\'}"
        val="${val#\'}"
        # Export into shell variable
        eval "${key}='${val}'"
    done < .env
fi

# Build env_vars using values from .env - one file to update
env_vars=(
    AZURE_VOICE_LIVE_ENDPOINT="${AZURE_VOICE_LIVE_ENDPOINT}"
    AZURE_VOICE_LIVE_API_KEY="${AZURE_VOICE_LIVE_API_KEY}"
    VOICE_LIVE_MODEL="${VOICE_LIVE_MODEL}"
    VOICE_LIVE_VOICE="${VOICE_LIVE_VOICE}"
    VOICE_LIVE_INSTRUCTIONS="${VOICE_LIVE_INSTRUCTIONS}"
)

echo "  - Retrieving ACR credentials so App Service can access the container image..."
# Use the retrieved ACR credentials to allow AppSvc to pull the image.
acr_user=$(az acr credential show -n $acr_name --query username -o tsv | tr -d '\r')
acr_pass=$(az acr credential show -n $acr_name --query passwords[0].value -o tsv | tr -d '\r')
acr_login_server=$(az acr show --name $acr_name --query "loginServer" --output tsv | tr -d '\r')
acr_image=${acr_login_server}/${image}:${tag}

echo "  - Creating App Service plan: $appsvc_plan Linux B1..."
az appservice plan create --name "$appsvc_plan" \
    --resource-group $rg \
    --is-linux \
    --sku B1 >/dev/null

echo "  - Creating Web App: ${webapp_name}..."
# Create the webapp with Docker runtime for container deployment
az webapp create --resource-group $rg \
    --plan $appsvc_plan \
    --name $webapp_name \
    --runtime "PYTHON:3.10" >/dev/null

echo "  - Applying environment variables to web app..."
az webapp config appsettings set --resource-group "$rg" \
    --name "$webapp_name" \
    --settings "${env_vars[@]}" >/dev/null

echo "  - Configuring Web App container settings to pull from ACR..."
az webapp config container set \
    --name "$webapp_name" \
    --resource-group "$rg" \
    --container-image-name "$acr_image" \
    --container-registry-url "https://$acr_login_server" \
    --container-registry-user "$acr_user" \
    --container-registry-password "$acr_pass" >/dev/null

echo "  - Configuring app settings..."
az webapp config set --resource-group "$rg" \
    --name "$webapp_name" \
    --startup-file "" \
    --always-on true >/dev/null

# Start / Restart to ensure container is pulled
sleep 5
echo "  - Restarting Web App to ensure new container image is pulled..."
az webapp restart --name "$webapp_name" --resource-group "$rg" >/dev/null
sleep 10 #Time for the service to restart and pull image


# Show final URL and cleanup info
echo
echo "Deployment complete!"
echo
echo " - AI Foundry with GPT Realtime model: PROVISIONED"
echo " - Flask app deployed to App Service: READY"
echo " - Your app is available at: https://${webapp_name}.azurewebsites.net"
echo
echo "Note: App may take a few minutes to start after loading the web page."
echo
