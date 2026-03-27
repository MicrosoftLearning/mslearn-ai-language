import os
from pathlib import Path
from playsound3 import playsound
from dotenv import load_dotenv

# Import namespaces
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Get Configuration Settings
        load_dotenv()
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        key = os.getenv("AZURE_OPENAI_API_KEY")
        model_deployment = os.getenv("MODEL_NAME")
        file_path = Path(__file__).parent / "speech.wav"
        
        # Play the speech file
        playsound(file_path)
        
        # Create the Azure OpenAI client
        token_provider = get_bearer_token_provider(                    
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider = token_provider,
            api_version="2025-03-01-preview"
        )
        
        # Call model to transcribe audio file
        audio_file = open(file_path, "rb")
        transcription = client.audio.transcriptions.create(
            model=model_deployment,
            file=audio_file,
            response_format="text"
        )
            
        print(transcription)

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()