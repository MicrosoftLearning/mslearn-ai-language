import os
import requests
import base64
from dotenv import load_dotenv

# Add references


def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        project_endpoint = os.getenv("PROJECT_ENDPOINT")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")

        # Initialize the project client


        # Get a chat client
        

        # Initialize prompts
        system_message = "You are an AI assistant for a produce supplier company."
        prompt = ""

        # Loop until the user types 'quit'
        while True:
            prompt = input("\nAsk a question about the audio\n(or type 'quit' to exit)\n")
            if prompt.lower() == "quit":
                break
            elif len(prompt) == 0:
                    print("Please enter a question.\n")
            else:
                print("Getting a response ...\n")

                # Encode the audio file


                # Get a response to audio input
                


    except Exception as ex:
        print(ex)


if __name__ == '__main__': 
    main()