import os
from dotenv import load_dotenv


# Import namespaces



def main():
    try:

        # Clear the console 
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        foundry_key = os.getenv('FOUNDRY_KEY')
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')

        # Configure translation
        


        # Configure speech for synthesis of translations
        


        # Translate user speech
        
        

        # Print and speak the translation results



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
