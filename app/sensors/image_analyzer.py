import cv2
import numpy as np

class ImageAnalyzer:
    """
    Offline image analyzer for detecting hazards.
    """

    def __init__(self):
        pass

    def is_food_spoiled(self, image_path):
        """
        Simple spoilage detection based on color and texture.
        Input:
            image_path: path to food image
        Returns:
            dict with spoilage likelihood and confidence.
        """
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "Image not found or invalid"}

        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Example heuristic: spoiled food tends to have brown/black mold areas.
        # We'll detect dark brown regions by HSV thresholding.

        # Define lower/upper HSV for brownish color
        lower_brown = np.array([10, 100, 20])
        upper_brown = np.array([30, 255, 200])
        mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)

        # Calculate percentage of brown pixels
        brown_ratio = np.sum(mask_brown > 0) / (image.shape[0] * image.shape[1])

        # Threshold to decide spoilage
        spoiled = brown_ratio > 0.05  # 5% brownish area

        return {
            "spoiled": spoiled,
            "brown_area_ratio": round(brown_ratio, 4),
            "advice": "Food likely spoiled" if spoiled else "Food looks okay"
        }

    def is_smoke_present(self, image_path):
        """
        Simple smoke detection using haze/light scatter effect.
        Input:
            image_path: path to image
        Returns:
            dict with smoke presence boolean and confidence.
        """
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "Image not found or invalid"}

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use variance of Laplacian to estimate blur (smoke/haze tends to blur edges)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()

        # Heuristic threshold - lower variance means more haze/smoke
        smoke_present = variance < 100  # Tune threshold based on dataset

        confidence = max(0, min(1, (100 - variance) / 100)) if smoke_present else 0

        return {
            "smoke_detected": smoke_present,
            "blur_variance": round(variance, 2),
            "confidence": round(confidence, 2),
            "advice": "Smoke or haze detected" if smoke_present else "No significant smoke detected"
        }