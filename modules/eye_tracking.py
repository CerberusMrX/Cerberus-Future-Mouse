import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from core.config import Config
from core.utils import calculate_distance

class EyeTracker:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True, # Vital for pure eyeball rotation tracking
            output_facial_transformation_matrixes=False,
            num_faces=1,
            min_face_detection_confidence=Config.FACE_MIN_DETECTION_CONFIDENCE,
            min_face_presence_confidence=Config.FACE_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=Config.FACE_MIN_TRACKING_CONFIDENCE
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)
        
        # Blink detection indices
        self.LEFT_EYE_TOP_BOTTOM = [(386, 374), (385, 373)]
        self.LEFT_EYE_LEFT_RIGHT = (362, 263)
        self.RIGHT_EYE_TOP_BOTTOM = [(159, 145), (158, 153)]
        self.RIGHT_EYE_LEFT_RIGHT = (33, 133)
        
        # Iris indices
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]
        
    def _calculate_ear(self, landmarks, top_bottom_pairs, left_right_pair):
        v_dist_1 = calculate_distance(landmarks[top_bottom_pairs[0][0]], landmarks[top_bottom_pairs[0][1]])
        v_dist_2 = calculate_distance(landmarks[top_bottom_pairs[1][0]], landmarks[top_bottom_pairs[1][1]])
        h_dist = calculate_distance(landmarks[left_right_pair[0]], landmarks[left_right_pair[1]])
        if h_dist == 0:
            return 0.0
        ear = (v_dist_1 + v_dist_2) / (2.0 * h_dist)
        return ear

    def process_frame(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        detection_result = self.detector.detect(mp_image)
        
        eye_data = None
        
        if detection_result.face_landmarks:
            face_landmarks = detection_result.face_landmarks[0]
            
            h, w, c = frame.shape
            landmarks = []
            
            for lm in face_landmarks:
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((cx, cy))
                
            left_ear = self._calculate_ear(landmarks, self.LEFT_EYE_TOP_BOTTOM, self.LEFT_EYE_LEFT_RIGHT)
            right_ear = self._calculate_ear(landmarks, self.RIGHT_EYE_TOP_BOTTOM, self.RIGHT_EYE_LEFT_RIGHT)
            
            avg_ear = (left_ear + right_ear) / 2.0
            is_blinking = avg_ear < Config.BLINK_THRESHOLD
            
            if len(landmarks) >= max(self.LEFT_IRIS):
                left_iris_pts = [landmarks[i] for i in self.LEFT_IRIS]
                iris_x = sum([p[0] for p in left_iris_pts]) / len(left_iris_pts)
                iris_y = sum([p[1] for p in left_iris_pts]) / len(left_iris_pts)
                absolute_iris_center = (int(iris_x), int(iris_y))
                
                # Extract pure eyeball rotation using Face Blendshapes (immune to head movement and blinks)
                if detection_result.face_blendshapes:
                    shapes = {b.category_name: b.score for b in detection_result.face_blendshapes[0]}
                    
                    look_out_l = shapes.get('eyeLookOutLeft', 0.0)
                    look_in_l = shapes.get('eyeLookInLeft', 0.0)
                    look_up_l = shapes.get('eyeLookUpLeft', 0.0)
                    look_down_l = shapes.get('eyeLookDownLeft', 0.0)
                    
                    look_out_r = shapes.get('eyeLookOutRight', 0.0)
                    look_in_r = shapes.get('eyeLookInRight', 0.0)
                    look_up_r = shapes.get('eyeLookUpRight', 0.0)
                    look_down_r = shapes.get('eyeLookDownRight', 0.0)
                    
                    # +X = Looking right (user's right), -X = Looking left (user's left)
                    gaze_x_l = look_in_l - look_out_l   # Left eye: in is right, out is left
                    gaze_x_r = look_out_r - look_in_r   # Right eye: out is right, in is left
                    avg_gaze_x = (gaze_x_l + gaze_x_r) / 2.0
                    
                    # +Y = Looking down, -Y = Looking up
                    gaze_y_l = look_down_l - look_up_l
                    gaze_y_r = look_down_r - look_up_r
                    avg_gaze_y = (gaze_y_l + gaze_y_r) / 2.0
                    
                    iris_center = (avg_gaze_x, avg_gaze_y)
                else:
                    iris_center = (0.0, 0.0)
            else:
                iris_center = None
                absolute_iris_center = None
                
            confidence = 1.0
            
            eye_data = {
                "landmarks": landmarks,
                "iris_center": iris_center,
                "absolute_iris_center": absolute_iris_center,
                "ear": avg_ear,
                "is_blinking": is_blinking,
                "raw_landmarks": face_landmarks,
                "confidence": confidence
            }
            
        return eye_data
