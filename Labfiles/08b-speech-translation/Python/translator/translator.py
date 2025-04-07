from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces


def main():
    try:
        global speech_config
        global translation_config

        # Get Configuration Settings
        load_dotenv()
        project_connection = os.getenv('PROJECT_CONNECTION')
        location = os.getenv('LOCATION')

        # Get AI Services key from the project
        
        
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
