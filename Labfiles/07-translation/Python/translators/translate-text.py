from dotenv import load_dotenv
import os

# import namespaces



def main():
    try:
        # Clear the console 
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')

        # Create client using endpoint and credential
        


        ## Choose target language



        # Translate text



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()