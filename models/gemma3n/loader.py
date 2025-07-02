from transformers import AutoTokenizer, AutoModelForCausalLM

def load_gemma(model_name="google/gemma-3n-E2B-it"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer