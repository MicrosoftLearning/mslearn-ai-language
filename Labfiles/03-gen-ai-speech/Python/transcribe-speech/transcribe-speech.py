import os
from pathlib import Path
from playsound3 import playsound
from dotenv import load_dotenv

# Import namespaces



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


        
        # Call model to transcribe audio file




    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()