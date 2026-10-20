"""
Face Recognizer Module — Local Binary Patterns Histograms (LBPH).
Handles user enrollment, face training, and identity verification.
"""

import os
import cv2
import numpy as np
from typing import Tuple, Optional

ENROLLED_DIR = os.path.join(os.path.dirname(__file__), 'data', 'enrolled')

class FaceRecognizerEngine:
    def __init__(self):
        os.makedirs(ENROLLED_DIR, exist_ok=True)
        # Create LBPH Recognizer using opencv-contrib-python
        self.recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
        self.labels_dict = {}
        self.is_trained = False
        self.train_model()

    def train_model(self):
        """Trains LBPH recognizer on images stored in data/enrolled/."""
        faces = []
        labels = []
        current_label_id = 0
        self.labels_dict = {}

        if not os.path.exists(ENROLLED_DIR):
            return

        for person_name in os.listdir(ENROLLED_DIR):
            person_path = os.path.join(ENROLLED_DIR, person_name)
            if not os.path.isdir(person_path):
                continue

            self.labels_dict[current_label_id] = person_name
            for img_name in os.listdir(person_path):
                img_path = os.path.join(person_path, img_name)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    img_resized = cv2.resize(img, (200, 200))
                    faces.append(img_resized)
                    labels.append(current_label_id)

            current_label_id += 1

        if len(faces) > 0:
            self.recognizer.train(faces, np.array(labels))
            self.is_trained = True
        else:
            self.is_trained = False

    def enroll_face(self, person_name: str, face_gray: np.ndarray) -> bool:
        """Enrolls a cropped face grayscale image under the given person_name."""
        if face_gray is None or face_gray.size == 0 or not person_name.strip():
            return False

        person_dir = os.path.join(ENROLLED_DIR, person_name.strip())
        os.makedirs(person_dir, exist_ok=True)

        count = len(os.listdir(person_dir)) + 1
        face_resized = cv2.resize(face_gray, (200, 200))
        file_path = os.path.join(person_dir, f"face_{count}.jpg")
        cv2.imwrite(file_path, face_resized)

        self.train_model()
        return True

    def predict(self, face_gray: np.ndarray, threshold: float = 80.0) -> Tuple[str, float]:
        """
        Predicts person identity from face crop using LBPH distance.
        Returns (person_name, confidence_score). Returns ('Unknown', score) if score > threshold.
        """
        if not self.is_trained or face_gray is None:
            return "Unknown", 0.0

        face_resized = cv2.resize(face_gray, (200, 200))
        label_id, distance = self.recognizer.predict(face_resized)

        # In LBPH, lower distance means higher confidence match
        if distance < threshold and label_id in self.labels_dict:
            name = self.labels_dict[label_id]
            confidence = round(max(0.0, 100.0 - distance), 2)
            return name, confidence

        return "Unknown", round(distance, 2)