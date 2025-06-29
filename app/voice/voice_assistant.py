import os
from whisper_cpp_python import Whisper
import pyttsx3
from app.models.gemma3n.gemma_wrapper import Gemma3nResponder  # We'll build this
from app.comms.panic_trigger import check_for_panic_keywords  # Optional

class VoiceAssistant:
    def __init__(self, model_path="models/ggml-small.en.bin", gemma_path="models/gemma3n/ggml-gemma3n.bin", child_mode=False):
        assert os.path.exists(model_path), f"Whisper model not found at: {model_path}"
        self.asr = Whisper(model_path=model_path)
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)
        self.tts.setProperty('volume', 1.0)
        self.child_mode = child_mode
        self.gemma = Gemma3nResponder(gemma_path)

    def transcribe_file(self, wav_path: str):
        assert os.path.exists(wav_path), f"Audio file not found at {wav_path}"
        with open(wav_path, "rb") as audio_file:
            result = self.asr.transcribe(audio_file)
        return result.get("text", "").strip()

    def process_and_respond(self, wav_path: str):
        transcript = self.transcribe_file(wav_path)
        if check_for_panic_keywords(transcript):
            response = "Panic alert triggered. Assistance is on the way."
        else:
            response = self.generate_response(transcript)
        self.speak(response)
        return transcript, response

    def generate_response(self, text: str) -> str:
        if not text:
            return "Sorry, I didn't hear anything."
        prompt = self.build_prompt(text)
        return self.gemma.generate(prompt)

    def build_prompt(self, user_text: str) -> str:
        if self.child_mode:
            return (
                "Speak gently like you're talking to a scared child during an emergency. "
                "Be comforting, brief, and clear. "
                f"The child said: {user_text}"
            )
        else:
            return f"You are a helpful crisis assistant. User said: {user_text}"

    def speak(self, text: str):
        self.tts.say(text)
        self.tts.runAndWait()