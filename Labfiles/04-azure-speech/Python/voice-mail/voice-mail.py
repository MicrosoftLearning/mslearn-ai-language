from dotenv import load_dotenv
import os
from playsound3 import playsound

# Import namespaces



def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')
        foundry_key = os.getenv('FOUNDRY_KEY')

        # Create speech_config using Entra ID authentication



        # Loop until user quits
        inputText = ""
        while inputText.lower() != "3":
            inputText = input("Choose an option:\n1: Record a greeting\n2: Transcribe messages\n3: Exit\n")
            if inputText != "3":
                if inputText == "1":
                    record_greeting(speech_config)
                elif inputText == "2":
                    transcribe_messages(speech_config)
                elif inputText == "3":
                    print("Exiting...")
                    return
                else:
                    print("Invalid option, please try again.")



    except Exception as ex:
        print(ex)

# record_greeting function
def record_greeting(speech_config):
    print("Recording greeting...")

    # Get greeting message from user
    greeting_message = input("Enter your greeting message: ")


    # Synthesize the greeting message to an audio file




# transcribe_messages function
def transcribe_messages(speech_config):
    print("Transcribing messages...")
    
    messages_folder = 'messages'
    for file_name in os.listdir(messages_folder):
        if file_name.endswith('.wav'):
            print(f"\nTranscribing {file_name}...")
            file_path = os.path.join(messages_folder, file_name)
            playsound(file_path)

            # Transcribe the audio file



if __name__ == "__main__":
    main()