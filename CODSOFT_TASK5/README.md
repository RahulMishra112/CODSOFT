# Task 5: Real-Time AI Face Detection and Recognition System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Haar%20Cascade%20%26%20LBPH-green)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-green)
![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local%20Processing-red)

A real-time Computer Vision system capable of detecting faces in images and live webcam streams using **OpenCV Haar Cascades** and recognizing enrolled individuals using **Local Binary Patterns Histograms (LBPH)**.

---

## 📌 Project Overview
This application provides a complete face identification solution with dual operational modes:
1. **Face Detection:** Identifies face regions in real time and draws annotated bounding boxes.
2. **Face Recognition & Enrollment:** Allows users to enroll participants live via webcam or photo uploads, building spatial LBP histograms for identity verification.

### Key Features
* **Haar Cascade Detection:** Rapid bounding box generation using multiscale feature classifiers.
* **LBPH Recognition Engine:** Computes texture intensity histograms across $8 \times 8$ spatial grids for robust participant matching.
* **Real-Time Web Streaming:** Asynchronous HTML5 Canvas frame loop delivering 15–20 FPS processing directly in the browser.
* **Participant Enrollment Portal:** Allows live user registration and identity updating on the fly.
* **Privacy Controls:** All biometric data and images are processed and stored locally on disk.

---

## 📁 Project Structure

```text
CODSOFT_TASK5/
├── app.py                  # Flask Application & Live Frame Processor
├── face_detector.py        # OpenCV Haar Cascade Detector Engine
├── face_recognizer.py      # LBPH Face Recognizer & Enrollment Engine
├── requirements.txt        # Project Dependencies
├── README.md               # Documentation
├── .gitignore              # Git Ignore Rules
├── models/
│   └── haarcascade_frontalface_default.xml # Detector Model XML
├── data/
│   └── enrolled/           # Local Enrolled Participant Biometric Data
├── templates/
│   └── index.html          # Web Interface
├── static/
│   ├── css/
│   │   └── style.css       # Interface Styling
│   └── js/
│       └── app.js          # Asynchronous Video Frame Loop
└── tests/
    └── test_face_detection.py # Automated Test Suite