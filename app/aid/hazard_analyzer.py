import cv2
import numpy as np
import torch

def analyze_image_for_hazards(image_path: str) -> str:
    img = cv2.imread(image_path)
    if img is None:
        return "Image could not be read."

    # Brightness
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)

    # Check for red/orange (possible fire/smoke)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 100, 100), (20, 255, 255))
    fire_alert = cv2.countNonZero(mask) > 500  # simple heuristic

    if brightness < 60:
        return "⚠️ It's quite dark. This might be a low-visibility situation."
    elif fire_alert:
        return "🔥 Possible fire or smoke detected!"
    elif brightness > 200:
        return "✅ Environment looks bright and clear."
    else:
        return "⚠️ Lighting is moderate. Check surroundings carefully."