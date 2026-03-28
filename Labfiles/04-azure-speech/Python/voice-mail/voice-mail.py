from dotenv import load_dotenv
import os
from playsound3 import playsound

# Import namespaces
from azure.identity import DefaultAzureCredential
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')
        foundry_key = os.getenv('FOUNDRY_KEY')

        # Create speech_config using Entra ID authentication
        credential = DefaultAzureCredential()
        speech_config = speech_sdk.SpeechConfig(
            token_credential=credential,
            endpoint=foundry_endpoint)

        # STT config using key-based auth (token_credential is unreliable for STT WebSocket)
        speech_config_stt = speech_sdk.SpeechConfig(
            subscription=foundry_key,
            endpoint=foundry_endpoint)

        # Loop until user quits
        inputText = ""
        while inputText.lower() != "3":
            inputText = input("Choose an option:\n1: Record a greeting\n2: Transcribe messages\n3: Exit\n")
            if inputText != "3":
                if inputText == "1":
                    record_greeting(speech_config)
                elif inputText == "2":
                    transcribe_messages(speech_config_stt)
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
    output_file = "greeting.wav"
    audio_config = speech_sdk.audio.AudioOutputConfig(filename=output_file)
    speech_config.speech_synthesis_voice_name = "en-US-Serena:DragonHDLatestNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config)
    result = speech_synthesizer.speak_text_async(greeting_message).get()
    if result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Greeting recorded and saved to {output_file}")
        speech_synthesizer = None  # Release the synthesizer resources
    else:
        print("Error recording greeting: {}".format(result.reason))

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
            audio_config = speech_sdk.audio.AudioConfig(filename=file_path)
            speech_recognizer = speech_sdk.SpeechRecognizer(speech_config=speech_config,
                                                            audio_config=audio_config)
            result = speech_recognizer.recognize_once_async().get()
            if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
                print(f"Transcription: {result.text}")
            elif result.reason == speech_sdk.ResultReason.Canceled:
                details = result.cancellation_details
                print(f"Canceled: {details.reason} — {details.error_details}")
            else:
                print("Error transcribing message: {}".format(result.reason))


if __name__ == "__main__":
    main()