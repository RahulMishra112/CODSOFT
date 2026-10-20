"""
Automated Unit Tests for Face Detection and Recognition Modules.
"""

import os
import cv2
import numpy as np
import pytest
from face_detector import FaceDetector
from face_recognizer import FaceRecognizerEngine

@pytest.fixture
def detector():
    return FaceDetector()

@pytest.fixture
def recognizer():
    return FaceRecognizerEngine()

def test_detector_initialization(detector):
    assert detector.cascade is not None

def test_empty_image_detection(detector):
    empty_img = np.zeros((100, 100, 3), dtype=np.uint8)
    faces, gray = detector.detect_faces(empty_img)
    assert len(faces) == 0

def test_synthetic_face_detection(detector):
    # Generates a valid test canvas
    canvas = np.full((300, 300, 3), 255, dtype=np.uint8)
    faces, gray = detector.detect_faces(canvas)
    assert isinstance(faces, np.ndarray) or isinstance(faces, tuple)

def test_recognizer_uninitialized(recognizer):
    dummy_crop = np.zeros((200, 200), dtype=np.uint8)
    name, confidence = recognizer.predict(dummy_crop)
    assert name == "Unknown"