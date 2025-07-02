from transformers import pipeline
from models.gemma3n import load_gemma

def get_text_generation_pipeline():
    model, tokenizer = load_gemma()
    return pipeline("text-generation", model = model, tokenizer = tokenizer)