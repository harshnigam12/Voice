"""
voice_listener.py

Continuous Voice Recognition using Vosk.

Features
--------
1. Offline speech recognition
2. Runs in background thread
3. Continuously listens
4. Stores latest command
5. Thread-safe

Author:
    Ishika Choudhary
"""

import json
import queue
import threading

import sounddevice as sd
from vosk import Model, KaldiRecognizer


class VoiceListener:

    def __init__(
        self,
        model_path="models/vosk-model-small-en-us-0.15",
        samplerate=16000
    ):

        # -----------------------------------
        # Load Vosk Model
        # -----------------------------------

        self.model = Model(model_path)

        self.recognizer = KaldiRecognizer(
            self.model,
            samplerate
        )

        self.samplerate = samplerate

        # -----------------------------------
        # Audio Queue
        # -----------------------------------

        self.audio_queue = queue.Queue()

        # -----------------------------------
        # Latest Recognized Command
        # -----------------------------------

        self.latest_command = None

        # -----------------------------------
        # Thread Control
        # -----------------------------------

        self.running = False

        self.thread = None

        # -----------------------------------
        # Lock for Thread Safety
        # -----------------------------------

        self.lock = threading.Lock()

    # ---------------------------------------------------
    # Callback from Microphone
    # ---------------------------------------------------

    def audio_callback(
        self,
        indata,
        frames,
        time,
        status
    ):

        if status:
            print(status)

        self.audio_queue.put(bytes(indata))

    # ---------------------------------------------------
    # Background Listening Loop
    # ---------------------------------------------------

    def listen_loop(self):

        print("\nVoice Listener Started")

        with sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self.audio_callback
        ):

            while self.running:

                data = self.audio_queue.get()

                if self.recognizer.AcceptWaveform(data):

                    result = json.loads(
                        self.recognizer.Result()
                    )

                    text = result.get(
                        "text",
                        ""
                    ).strip().lower()

                    # Normalize common Vosk misrecognitions

                    if text in [
                        "big apple",
                        "pick up apple",
                        "pick apple"
                    ]:
                        text = "get apple"

                    elif text in [
                        "big banana",
                        "pick up banana",
                        "pick banana"
                    ]:
                        text = "get banana"

                    elif text in [
                        "big orange",
                        "pick up orange",
                        "pick orange"
                    ]:
                        text = "get orange"

                    if text != "":

                        with self.lock:
                            self.latest_command = text

                        print(
                            "\nVoice Command :",
                            text
                        )

    # ---------------------------------------------------
    # Start Listener
    # ---------------------------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.listen_loop,
            daemon=True
        )

        self.thread.start()

    # ---------------------------------------------------
    # Stop Listener
    # ---------------------------------------------------

    def stop(self):

        self.running = False

        if self.thread is not None:
            self.thread.join()

        print("Voice Listener Stopped")

    # ---------------------------------------------------
    # Return Latest Command
    # ---------------------------------------------------

    def get_command(self):

        with self.lock:

            command = self.latest_command

            self.latest_command = None

        return command


# -------------------------------------------------------
# Testing
# -------------------------------------------------------

if __name__ == "__main__":

    voice = VoiceListener()

    voice.start()

    print("\nSay something...\n")

    try:

        while True:

            command = voice.get_command()

            if command:

                print(
                    "Recognized :",q
                    command
                )

    except KeyboardInterrupt:

        voice.stop()