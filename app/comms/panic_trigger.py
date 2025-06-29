import sounddevice as sd
import queue
import sys
import os
from vosk import Model, KaldiRecognizer
import json
import asyncio
from app.comms.mesh_comm import MeshComm

q = queue.Queue()

class PanicTrigger:
    def __init__(self, vosk_model_dir="models/vosk"):
        if not os.path.exists(vosk_model_dir):
            raise FileNotFoundError("Vosk model not found")
        self.model = Model(vosk_model_dir)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.mesh = MeshComm()

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"[VOSK] {status}", file=sys.stderr)
        q.put(bytes(indata))

    def listen_for_panic(self):
        print("[Voice Trigger] Listening for 'help me'...")

        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=self._audio_callback):
            while True:
                data = q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").lower()
                    print(f"[Voice] Heard: {text}")

                    if "help me" in text:
                        asyncio.run(self.trigger_panic_alert())

    async def trigger_panic_alert(self):
        print("[PANIC] Triggered!")
        os.system("play -nq -t alsa synth 1 sine 1000")  # Play loud beep
        await self.mesh.broadcast_alert("Panic! Someone nearby needs help.")