import cv2
import torch
import numpy as np
from typing import Union

class Gemma3nModel:
    def __init__(self, model_path=None, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

    def predict(self, image_tensor: torch.Tensor) -> str:
        mean_brightness = image_tensor.mean().item()
        if mean_brightness < 0.3:
            return "⚠️ Image is dark. Might indicate low visibility or nighttime."
        elif mean_brightness > 0.7:
            return "✅ Image is bright and clear. No immediate hazard detected."
        else:
            return "⚠️ Moderate lighting. Please inspect for potential hazards."

def preprocess_image_from_bytes(image_bytes: bytes) -> torch.Tensor:
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to decode image bytes")
    return preprocess_cv_image(img)

def preprocess_image_from_path(image_path: str) -> torch.Tensor:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    return preprocess_cv_image(img)

def preprocess_cv_image(img: np.ndarray) -> torch.Tensor:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    return torch.tensor(img, dtype=torch.float32).unsqueeze(0)

def scan_aid_image(image_input: Union[str, bytes], model: Gemma3nModel) -> str:
    if isinstance(image_input, str):
        img_tensor = preprocess_image_from_path(image_input).to(model.device)
    elif isinstance(image_input, bytes):
        img_tensor = preprocess_image_from_bytes(image_input).to(model.device)
    else:
        raise TypeError("image_input must be file path or bytes")
    return model.predict(img_tensor)

if __name__ == "__main__":
    model = Gemma3nModel()
    test_img_path = "test_image.jpg"
    try:
        result = scan_aid_image(test_img_path, model)
        print("Result:", result)
    except Exception as e:
        print("Error:", e)