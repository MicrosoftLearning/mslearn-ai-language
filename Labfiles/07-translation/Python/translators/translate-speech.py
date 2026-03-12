from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces


def main():
    try:
        global speech_config
        global translation_config

        # Clear the console 
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        foundry_key = os.getenv('FOUNDRY_KEY')
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')

        # Configure translation


        # Configure speech


        # Get user input
        targetLanguage = ''
        while targetLanguage != 'quit':
            targetLanguage = input('\nEnter a target language\n fr = French\n es = Spanish\n hi = Hindi\n Enter anything else to stop\n').lower()
            if targetLanguage in translation_config.target_languages:
                Translate(targetLanguage)
            else:
                targetLanguage = 'quit'
                

    except Exception as ex:
        print(ex)

def Translate(targetLanguage):
    translation = ''

    # Translate speech


    # Synthesize translation



if __name__ == "__main__":
    main()
