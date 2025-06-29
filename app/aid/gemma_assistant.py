import torch
from transformers import AutoProcessor, AutoModelForSeq2SeqLM
from PIL import Image

class Gemma3nOffline:
    def __init__(self, model_dir="models/gemma3n", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained(model_dir)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir).to(self.device)
        self.model.eval()

    def generate_response(self, prompt: str) -> str:
        # If visual input is unnecessary, remove it later
        inputs = self.processor(text=prompt, images=Image.new("RGB", (1, 1)), return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=64)
        return self.processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()