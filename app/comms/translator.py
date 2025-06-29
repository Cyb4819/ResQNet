import sounddevice as sd
import queue
import json
import os
import sys
import pyttsx3
from vosk import Model as VoskModel, KaldiRecognizer
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch

q = queue.Queue()

class Translator:
    def __init__(self, vosk_model_dir="models/vosk", gemma_dir="models/gemma3n"):
        if not os.path.exists(vosk_model_dir):
            raise FileNotFoundError("Vosk model not found at " + vosk_model_dir)
        if not os.path.exists(gemma_dir):
            raise FileNotFoundError("Gemma 3n model not found at " + gemma_dir)

        # STT
        self.stt_model = VoskModel(vosk_model_dir)
        self.recognizer = KaldiRecognizer(self.stt_model, 16000)

        # TTS
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)

        # Gemma 3n for translation
        self.processor = AutoProcessor.from_pretrained(gemma_dir)
        self.model = AutoModelForVision2Seq.from_pretrained(gemma_dir).to("cpu")
        self.model.eval()

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"[STT] {status}", file=sys.stderr)
        q.put(bytes(indata))

    def listen_and_transcribe(self) -> str:
        print("[Translator] Listening...")
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=self._audio_callback):
            while True:
                data = q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "")
                    if text:
                        print(f"[STT] You said: {text}")
                        return text

    def translate_text(self, input_text: str, target_lang: str = "English") -> str:
        prompt = f"Translate the following sentence into {target_lang}: {input_text}"
        inputs = self.processor(text=prompt, images=Image.new("RGB", (1, 1)), return_tensors="pt").to("cpu")

        with torch.no_grad():
            output_ids = self.model.generate(**inputs, max_new_tokens=64)
            output_text = self.processor.batch_decode(output_ids, skip_special_tokens=True)[0]

        return output_text.strip()

    def speak(self, text: str):
        print(f"[TTS] Speaking: {text}")
        self.tts.say(text)
        self.tts.runAndWait()

    def voice_translate(self, target_lang: str = "English"):
        spoken_text = self.listen_and_transcribe()
        translated = self.translate_text(spoken_text, target_lang=target_lang)
        self.speak(translated)
        return {"original": spoken_text, "translated": translated}