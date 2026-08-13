import os
import asyncio
import base64
import queue
from dotenv import load_dotenv
import pyaudio

# Import namespaces


def main():
    """Main entry point."""

    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get required configuration from environment variables
        load_dotenv()
        endpoint = os.environ.get("VOICELIVE_ENDPOINT")
        agent_name = os.environ.get("VOICELIVE_AGENT_NAME")
        project_name = os.environ.get("VOICELIVE_PROJECT_NAME")

        # Create credential for authentication
        credential = AzureCliCredential()

        # Create and start the voice concierge
        concierge = VoiceConcierge(
            endpoint=endpoint,
            credential=credential,
            agent_name=agent_name,
            project_name=project_name,
        )

        # Run the concierge
        try:
            asyncio.run(concierge.start())
        except KeyboardInterrupt:
            # Exit if the user enters CTRL+C
            print("\n[stop] Goodbye!")

    except Exception as e:
        print(f"[error] An error occurred: {e}")


# VoiceConcierge class - main coordinator for the voice agent
class VoiceConcierge:
    """
    Main voice concierge that coordinates the conversation flow.

    This class demonstrates the essential pattern for Azure Speech Voice Live:
    1. Connect to the service
    2. Configure the session
    3. Start audio capture/playback
    4. Process events from the service
    """

    def __init__(self, endpoint, credential, agent_name, project_name):
        self.endpoint = endpoint
        self.credential = credential
        self.agent_name = agent_name
        self.project_name = project_name

    async def start(self):
        """Start the voice concierge."""
        print("\n" + "=" * 60)
        print(f"  ALPINE SKI HOUSE VOICE CONCIERGE - {self.agent_name}")
        print("=" * 60)

        # Add your code in this try block!
        try:
            # STEP 1: Connect Azure Speech Voice Live to the agent

            # STEP 2: Initialize audio processor

            # STEP 3: Configure the session

            # STEP 4: Start audio systems

            # STEP 5: Process events

            pass  # Remove this line once you have added the code for steps 1-5

        finally:
            if hasattr(self, 'audio_processor'):
                self.audio_processor.shutdown()

    async def setup_session(self):
        """Configure the session with audio settings."""

        session_config = RequestSession(
            # Enable both text and audio
            modalities=[Modality.TEXT, Modality.AUDIO],

            # Audio format (16-bit PCM at 24kHz)
            input_audio_format=InputAudioFormat.PCM16,
            output_audio_format=OutputAudioFormat.PCM16,

            # Voice activity detection (when to detect speech)
            turn_detection=AzureSemanticVadMultilingual(),

            # Prevent echo from speaker feedback
            input_audio_echo_cancellation=AudioEchoCancellation(),

            # Reduce background noise
            input_audio_noise_reduction=AudioNoiseReduction(type="azure_deep_noise_suppression")
        )

        await self.connection.session.update(session=session_config)
        print("[ok] Session configured")

    async def process_events(self):
        """Process events from the Voice Live service."""

        # Listen for events from the service
        async for event in self.connection:
            await self.handle_event(event)

    async def handle_event(self, event):
        """Handle different event types from the service."""

        # Session is ready - start capturing audio
        if event.type == ServerEventType.SESSION_UPDATED:
            print(f"[connected] Agent: {event.session.agent.name}")
            self.audio_processor.start_capture()

        # Guest speech was transcribed
        elif event.type == ServerEventType.CONVERSATION_ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED:
            print(f'[guest] {event.get("transcript", "")}')

        # Agent is responding with audio transcript
        elif event.type == ServerEventType.RESPONSE_AUDIO_TRANSCRIPT_DONE:
            print(f'[agent] {event.get("transcript", "")}')

        # Guest started speaking (interrupt any playing audio)
        elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
            self.audio_processor.clear_playback_queue()
            print("[listening]")

        # Guest stopped speaking
        elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STOPPED:
            print("[thinking]")

        # Receiving audio response chunks
        elif event.type == ServerEventType.RESPONSE_AUDIO_DELTA:
            self.audio_processor.queue_audio(event.delta)

        # Audio response complete
        elif event.type == ServerEventType.RESPONSE_AUDIO_DONE:
            print("[done] Response complete\n")

        # Handle errors
        elif event.type == ServerEventType.ERROR:
            print(f"[error] {event.error.message}")


# AudioProcessor class - handles microphone input and speaker output using PyAudio
class AudioProcessor:
    """
    Handles audio input (microphone) and output (speakers).

    Key responsibilities:
    - Capture audio from the microphone and send it to Voice Live
    - Receive audio from Voice Live and play it through the speakers
    """

    def __init__(self, connection):
        self.connection = connection
        self.audio = pyaudio.PyAudio()

        # Audio settings: 24kHz, 16-bit PCM, mono
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 24000
        self.chunk_size = 1200  # 50ms chunks

        # Streams for input and output
        self.input_stream = None
        self.output_stream = None
        self.playback_queue = queue.Queue()

    def start_capture(self):
        """Start capturing audio from the microphone."""

        def capture_callback(in_data, frame_count, time_info, status):
            # Convert audio to base64 and send to Voice Live
            audio_base64 = base64.b64encode(in_data).decode("utf-8")
            asyncio.run_coroutine_threadsafe(
                self.connection.input_audio_buffer.append(audio=audio_base64),
                self.loop
            )
            return (None, pyaudio.paContinue)

        # Store event loop for use in callback thread
        self.loop = asyncio.get_event_loop()

        self.input_stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=capture_callback
        )
        print("[ok] Microphone started")

    def start_playback(self):
        """Start audio playback system."""

        remaining = bytes()

        def playback_callback(in_data, frame_count, time_info, status):
            nonlocal remaining

            # Calculate bytes needed
            bytes_needed = frame_count * pyaudio.get_sample_size(pyaudio.paInt16)
            output = remaining[:bytes_needed]
            remaining = remaining[bytes_needed:]

            # Get more audio from queue if needed
            while len(output) < bytes_needed:
                try:
                    audio_data = self.playback_queue.get_nowait()
                    if audio_data is None:  # End signal
                        break
                    output += audio_data
                except queue.Empty:
                    # Pad with silence if no audio available
                    output += bytes(bytes_needed - len(output))
                    break

            # Keep any extra for next callback
            if len(output) > bytes_needed:
                remaining = output[bytes_needed:]
                output = output[:bytes_needed]

            return (output, pyaudio.paContinue)

        self.output_stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=playback_callback
        )
        print("[ok] Speakers ready")

    def queue_audio(self, audio_data):
        """Add audio data to the playback queue."""
        self.playback_queue.put(audio_data)

    def clear_playback_queue(self):
        """Clear any pending audio (used when the guest interrupts)."""
        while not self.playback_queue.empty():
            try:
                self.playback_queue.get_nowait()
            except queue.Empty:
                break

    def shutdown(self):
        """Clean up audio resources."""
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()

        if self.output_stream:
            self.playback_queue.put(None)  # Signal end
            self.output_stream.stop_stream()
            self.output_stream.close()

        self.audio.terminate()
        print("[stop] Audio stopped")


if __name__ == "__main__":
    main()
