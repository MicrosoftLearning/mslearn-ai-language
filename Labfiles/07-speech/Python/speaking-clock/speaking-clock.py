from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential  # noqa: F401 (imported for future exercises)
import azure.cognitiveservices.speech as speech_sdk


def main():
    """Entry point for the speaking clock sample."""

    # Clear any previous console output so the steps below are easy to follow.
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        global speech_config

        # Load KEY and REGION values from the .env file instead of hardcoding secrets.
        load_dotenv()
        speech_key = os.getenv('KEY')
        speech_region = os.getenv('REGION')

        # Configure the Azure Speech service using the developer-provided key/region.
        speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
        print('Ready to use speech service in:', speech_config.region)

        # Transcribe the spoken command captured in time.wav.
        command = TranscribeCommand()

        # Act on the recognized phrase (case-insensitive) when it matches our wake phrase.
        if command.lower() == 'what time is it?':
            TellTime()

    except Exception as ex:
        # Catch and print unexpected errors so the learner sees what went wrong.
        print(ex)


def TranscribeCommand():
    """Recognize the spoken command stored in time.wav and return the text."""

    command = ''

    # Build the absolute path to the sample audio file that contains the command.
    current_dir = os.getcwd()
    audioFile = current_dir + '/time.wav'

    # Create a speech recognizer that will listen to the provided WAV file.
    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)

    # Ask the recognizer to process the audio once and wait synchronously for the result.
    print("Listening...")
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print("Command: ", command)
    else:
        # Display the reason (for example, NoMatch or Canceled) to help with debugging.
        print("reason: ", speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    # Return the recognized phrase (or an empty string if recognition failed).
    return command


def TellTime():
    """Synthesize the current time into an audio response."""

    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour, now.minute)

    # Configure the speech synthesizer to write audio to output.wav using a Neural voice.
    output_file = "output.wav"
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    audio_config = speech_sdk.audio.AudioConfig(filename=output_file)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)

    # Speak the response text and report whether synthesis succeeded.
    # Synthesize spoken output
    responseSsml = " \
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
            <voice name='en-GB-LibbyNeural'> \
                {} \
                <break strength='weak'/> \
                Time to end this lab! \
            </voice> \
        </speak>".format(response_text)
    speak = speech_synthesizer.speak_ssml_async(responseSsml).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    else:
        print("Spoken output saved in " + output_file)


if __name__ == "__main__":
    main()
