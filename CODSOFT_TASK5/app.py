"""
Flask Web Application Server for Face Detection and Recognition.
"""

import base64
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
from face_detector import FaceDetector
from face_recognizer import FaceRecognizerEngine

app = Flask(__name__)
detector = FaceDetector()
recognizer = FaceRecognizerEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/detect', methods=['POST'])
def detect_and_recognize():
    """Endpoint: Receives image upload/base64 frame, detects faces, draws bounding boxes & recognizes."""
    data = request.get_json()
    image_data = data.get('image', '')

    if not image_data:
        return jsonify({'error': 'No image provided.'}), 400

    try:
        # Decode base64 image string
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img_bgr is None:
            return jsonify({'error': 'Invalid image format.'}), 400

        faces, gray = detector.detect_faces(img_bgr)
        results = []

        # Draw bounding boxes and predict identities
        for (x, y, w, h) in faces:
            face_crop = gray[y:y+h, x:x+w]
            name, confidence = recognizer.predict(face_crop)

            # Visual annotations
            color = (0, 242, 254) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(img_bgr, (x, y), (x+w, y+h), color, 2)
            
            label = f"{name} ({confidence}%)" if name != "Unknown" else "Unknown"
            cv2.putText(img_bgr, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            results.append({
                'bbox': [int(x), int(y), int(w), int(h)],
                'name': name,
                'confidence': float(confidence)
            })

        # Encode processed image to base64
        _, buffer = cv2.imencode('.jpg', img_bgr)
        processed_b64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            'count': len(faces),
            'processed_image': f"data:image/jpeg;base64,{processed_b64}",
            'faces': results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enroll', methods=['POST'])
def enroll():
    """Endpoint: Enrolls face crop from provided image under participant name."""
    data = request.get_json()
    name = data.get('name', '').strip()
    image_data = data.get('image', '')

    if not name or not image_data:
        return jsonify({'error': 'Name and image are required for enrollment.'}), 400

    try:
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        faces, gray = detector.detect_faces(img_bgr)

        if len(faces) == 0:
            return jsonify({'error': 'No face detected in enrollment image.'}), 400

        # Use largest detected face
        x, y, w, h = sorted(faces, key=lambda b: b[2]*b[3], reverse=True)[0]
        face_crop = gray[y:y+h, x:x+w]

        success = recognizer.enroll_face(name, face_crop)
        if success:
            return jsonify({'message': f'Successfully enrolled "{name}"!'})
        return jsonify({'error': 'Enrollment failed.'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)