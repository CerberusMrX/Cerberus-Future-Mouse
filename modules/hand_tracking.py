import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from core.config import Config

class HandTracker:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=Config.HAND_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=Config.HAND_MIN_TRACKING_CONFIDENCE,
            min_hand_presence_confidence=Config.HAND_MIN_DETECTION_CONFIDENCE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
    def process_frame(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        detection_result = self.detector.detect(mp_image)
        
        hand_data = None
        
        if detection_result.hand_landmarks:
            hand_landmarks = detection_result.hand_landmarks[0]
            
            h, w, c = frame.shape
            landmarks = []
            
            for lm in hand_landmarks:
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((cx, cy))
                
            confidence = 1.0 # The task API returns valid confidence scores but 1.0 is sufficient for our logic model
            
            hand_data = {
                "landmarks": landmarks,
                "index_tip": landmarks[8] if len(landmarks) > 8 else None,
                "thumb_tip": landmarks[4] if len(landmarks) > 4 else None,
                "middle_tip": landmarks[12] if len(landmarks) > 12 else None,
                "raw_landmarks": hand_landmarks,
                "confidence": confidence
            }
            
        return hand_data
