import cv2

class AutoCalibrator:
    def __init__(self, required_frames=60):
        self.is_calibrated = False
        self.required_frames = required_frames
        self.frame_count = 0
        
        # We need to find the natural resting position of the eye to use as an offset
        self.eye_positions = []
        self.eye_neutral_pos = None

    def update(self, eye_data):
        """
        Update the calibration phase with new frame data.
        Returns True if calibration is complete.
        """
        if self.is_calibrated:
            return True
            
        if eye_data and 'iris_center' in eye_data and eye_data['iris_center']:
            self.eye_positions.append(eye_data['iris_center'])
            self.frame_count += 1
            
        if self.frame_count >= self.required_frames:
            # Calculate average neutral eye position (keep as floats for high precision relative vectors)
            avg_x = sum([p[0] for p in self.eye_positions]) / len(self.eye_positions)
            avg_y = sum([p[1] for p in self.eye_positions]) / len(self.eye_positions)
            self.eye_neutral_pos = (avg_x, avg_y)
            self.is_calibrated = True
            print(f"Calibration Complete. Neutral Gaze set to: {self.eye_neutral_pos}")
            return True
            
        return False
        
    def get_progress(self):
        """Returns a value between 0.0 and 1.0 indicating completion."""
        return min(1.0, self.frame_count / self.required_frames)
        
    def draw_calibration_ui(self, frame):
        """Draws the calibration instruction and progress bar on the frame."""
        h, w, _ = frame.shape
        cv2.putText(frame, "CALIBRATING... LOOK AT THE CENTER OF THE SCREEN", (50, h // 2 - 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    
        # Draw progress bar
        progress = self.get_progress()
        bar_w = int(400 * progress)
        start_x = w // 2 - 200
        start_y = h // 2
        cv2.rectangle(frame, (start_x, start_y), (start_x + 400, start_y + 30), (100, 100, 100), 2)
        cv2.rectangle(frame, (start_x, start_y), (start_x + bar_w, start_y + 30), (0, 255, 0), -1)
        
        return frame
