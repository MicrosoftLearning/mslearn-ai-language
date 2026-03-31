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
        agent_name = os.getenv('AGENT_NAME')
        

        # Get project client
        
        
        # Get an OpenAI client
        
        
        # Main loop
        while True:
            # Get user input
            prompt = input("User prompt (or 'quit'): ")
            if prompt == "quit" or len(prompt) == 0:
                break
            else:
                # Use the agent to get a response
                
                
                
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()