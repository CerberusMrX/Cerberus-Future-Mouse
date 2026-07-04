import cv2
import numpy as np

class UIOverlay:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        
    def draw(self, frame, hand_data, eye_data, active_mode, fps):
        # Draw hand landmarks
        if hand_data and 'landmarks' in hand_data:
            for (x, y) in hand_data['landmarks']:
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
            # Highlight index tip (cursor anchor point)
            if hand_data['index_tip']:
                cv2.circle(frame, hand_data['index_tip'], 8, (255, 0, 0), 2)
                
        # Draw eye gaze
        if eye_data and 'absolute_iris_center' in eye_data and eye_data['absolute_iris_center']:
            cv2.circle(frame, eye_data['absolute_iris_center'], 4, (0, 0, 255), -1)
            
        # Draw HUD Information
        cv2.putText(frame, f"MODE: {active_mode}", (20, 40), self.font, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 80), self.font, 1, (0, 255, 255), 2)
        
        # Hardware warnings or statuses
        if eye_data and eye_data.get('is_blinking'):
            cv2.putText(frame, "BLINK DETECTED", (20, 120), self.font, 1, (0, 0, 255), 2)
            
        # Help text
        cv2.putText(frame, "Press 'Q' to Exit", (frame.shape[1] - 250, 40), self.font, 0.8, (200, 200, 200), 2)
        
        return frame
