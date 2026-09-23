import os
from dotenv import load_dotenv

# Import namespaces


def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        speech_endpoint = os.getenv('SPEECH_ENDPOINT')

        # Configure translation



        # Configure speech for synthesis of translations



        # Translate guest speech



        # Print and speak the translation results



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
