import os
from urllib.request import urlopen, Request
import base64

# Add references


def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        project_connection = os.getenv("PROJECT_CONNECTION")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")
        
        # Initialize the project client

        

        ## Get a chat client
        


        # Initialize prompts
        system_message = "You are an AI assistent in a grocery store that sells fruit."
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


                # Get a response to audio input
                


    except Exception as ex:
        print(ex)


if __name__ == '__main__': 
    main()