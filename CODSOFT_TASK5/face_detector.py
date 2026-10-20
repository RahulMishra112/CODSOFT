"""
Face Detector Module — OpenCV Haar Cascade Implementation.
Automatically downloads and validates official Haar Cascade XML data.
"""

import os
import ssl
import urllib.request
import cv2
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
CASCADE_PATH = os.path.join(MODEL_DIR, 'haarcascade_frontalface_default.xml')
OFFICIAL_URL = "https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml"

def ensure_model_file():
    """Downloads official OpenCV Haar Cascade XML if missing or corrupt."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Download if file is missing or smaller than 100KB (corrupt/HTML redirect)
    if not os.path.exists(CASCADE_PATH) or os.path.getsize(CASCADE_PATH) < 100000:
        print("Downloading official Haar Cascade XML model file...")
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(OFFICIAL_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            content = response.read()
            with open(CASCADE_PATH, 'wb') as f:
                f.write(content)
        print(f"Model successfully saved to {CASCADE_PATH} ({len(content)} bytes)!")

class FaceDetector:
    def __init__(self):
        ensure_model_file()
        
        # 1. Load from local downloaded XML
        self.cascade = cv2.CascadeClassifier(CASCADE_PATH)
        
        # 2. Backup check with builtin cv2 path if local fail occurs
        if self.cascade.empty() and hasattr(cv2, 'data') and hasattr(cv2.data, 'haarcascades'):
            builtin_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
            self.cascade = cv2.CascadeClassifier(builtin_path)

        if self.cascade.empty():
            raise RuntimeError("Failed to load OpenCV Haar Cascade model file.")

    def detect_faces(self, image_np: np.ndarray, scale_factor: float = 1.1, min_neighbors: int = 5):
        """
        Detects faces in an OpenCV image array (BGR).
        Returns bounding boxes [(x, y, w, h), ...] and gray image.
        """
        if image_np is None or image_np.size == 0:
            return [], None

        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=(30, 30)
        )
        return faces, gray