# camera_handler.py
import cv2
import time
import numpy as np
from roboflow import Roboflow

class CacaoClassifier:
    def __init__(self):
        self.rf = Roboflow(api_key="f4UBb9Y1BqAaVoiasTC1")
        project = self.rf.workspace("cacaotrain").project("trained-q5iwo")
        self.model = project.version(2).model

        self.hsv_thresholds = {
            "Criollo": (np.array([0, 10, 180]), np.array([15, 80, 255])),
            "Forastero": (np.array([130, 50, 50]), np.array([170, 255, 255])),
            "Trinitario": (np.array([10, 50, 100]), np.array([30, 255, 255]))
        }

        self.min_match_threshold = 10.0
        self.last_prediction_time = 0

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def detect_bean(self):
        ret, frame = self.cap.read()
        if not ret:
            return "Unknown"

        now = time.time()
        if now - self.last_prediction_time < 1.5:
            return None

        self.last_prediction_time = now
        image_path = "temp_frame.jpg"
        cv2.imwrite(image_path, frame)

        try:
            predictions = self.model.predict(image_path, confidence=40, overlap=30).json()
        except Exception as e:
            print(f"[Detection Error] {e}")
            return "Unknown"

        for pred in predictions.get("predictions", []):
            x, y, w, h = map(int, [pred['x'], pred['y'], pred['width'], pred['height']])
            x1, y1 = max(x - w // 2, 0), max(y - h // 2, 0)
            x2, y2 = x + w // 2, y + h // 2
            crop = frame[y1:y2, x1:x2]
            hsv_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

            for label, (lower, upper) in self.hsv_thresholds.items():
                mask = cv2.inRange(hsv_crop, lower, upper)
                match_ratio = (cv2.countNonZero(mask) / (crop.size / 3)) * 100
                if match_ratio > self.min_match_threshold:
                    return label

        return "Unknown"

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
