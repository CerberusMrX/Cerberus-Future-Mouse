import cv2
import time
import sys
from core.config import Config
from modules.hand_tracking import HandTracker
from modules.eye_tracking import EyeTracker
from modules.fusion_engine import FusionEngine
from modules.gesture_engine import GestureEngine
from modules.cursor_control import CursorController
from modules.ui_overlay import UIOverlay
from modules.auto_calibration import AutoCalibrator

def main():
    print("Initiating Cerberus Future Mouse Engine...")
    cap = cv2.VideoCapture(Config.CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.FRAME_HEIGHT)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        sys.exit(1)
        
    hand_tracker = HandTracker()
    eye_tracker = EyeTracker()
    fusion_engine = FusionEngine()
    gesture_engine = GestureEngine()
    cursor_controller = CursorController()
    ui_overlay = UIOverlay()
    calibrator = AutoCalibrator(required_frames=60)
    
    prev_time = time.time()
    
    cv2.namedWindow("Cerberus Future Mouse", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Cerberus Future Mouse", 800, 600) # Restored desktop view
    
    system_state = 'OFF' # Start off as requested
    print("=========================================")
    print("System loaded and starting in OFF state.")
    print("Controls:")
    print("[1] HAND Only Mode")
    print("[2] EYE Only Mode")
    print("[3] HYBRID Mode (Eye & Hand)")
    print("[0] Turn OFF")
    print("[Q] Exit Application")
    print("\n--- EYE CLICK OPTIONS (Active in Modes 2 & 3) ---")
    print("-> BLINK to target and left-click")
    print("-> STARE at a spot for >0.5 seconds to auto-click")
    print("=========================================")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        hand_data = hand_tracker.process_frame(frame)
        eye_data = eye_tracker.process_frame(frame)
        
        # Keyboard inputs
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27: # Exit on 'q' or 'Esc'
            break
        elif key == ord('1'):
            system_state = 'HAND'
        elif key == ord('2'):
            system_state = 'EYE'
        elif key == ord('3'):
            system_state = 'HYBRID'
        elif key == ord('0'):
            system_state = 'OFF'
        
        if not calibrator.is_calibrated:
            calibrator.update(eye_data)
            display_frame = calibrator.draw_calibration_ui(frame)
            cv2.imshow("Cerberus Future Mouse", display_frame)
            continue
        
        active_mode = "DISABLED"
        
        if system_state != 'OFF':
            # Translating to screen space
            cam_hand_pos = hand_data['index_tip'] if hand_data else None
            cam_eye_pos = eye_data['iris_center'] if (eye_data and eye_data['iris_center']) else None
            
            screen_hand_pos = None
            if cam_hand_pos and system_state in ['HAND', 'HYBRID']:
                screen_hand_pos = cursor_controller.map_camera_to_screen(cam_hand_pos[0], cam_hand_pos[1], w, h)
                
            screen_eye_pos = None
            if cam_eye_pos and calibrator.eye_neutral_pos and system_state in ['EYE', 'HYBRID']:
                offset_x = cam_eye_pos[0] - calibrator.eye_neutral_pos[0]
                offset_y = cam_eye_pos[1] - calibrator.eye_neutral_pos[1]
                
                # Blendshape gaze offsets range roughly from -0.8 to +0.8 depending on extreme looks
                sensitivity_x = 8.0 # Balanced mapping
                sensitivity_y = -7.0 
                
                # Mild acceleration curve (1.3) allows high precision clicking without sacrificing screen-edge reach
                sign_x = 1 if offset_x >= 0 else -1
                sign_y = 1 if offset_y >= 0 else -1
                
                scaled_offset_x = sign_x * (abs(offset_x) ** 1.3)
                scaled_offset_y = sign_y * (abs(offset_y) ** 1.3)
                
                eye_screen_x = int(w/2 + (scaled_offset_x * w * sensitivity_x))
                eye_screen_y = int(h/2 + (scaled_offset_y * h * sensitivity_y))
                
                screen_eye_pos = cursor_controller.map_camera_to_screen(eye_screen_x, eye_screen_y, w, h, deadzone=0)
                
            # Fusion
            final_pos, active_mode = fusion_engine.fuse(
                screen_hand_pos, 
                screen_eye_pos,
                hand_conf=hand_data['confidence'] if hand_data else 0.0,
                eye_conf=eye_data['confidence'] if eye_data else 0.0
            )
            
            # Action Execution
            if final_pos:
                cursor_controller.move_to(final_pos[0], final_pos[1])
                
            if system_state in ['HAND', 'HYBRID']:
                hand_action = gesture_engine.process_hand_gestures(hand_data)
                if hand_action == 'left_click':
                    cursor_controller.click('left')
                elif hand_action == 'right_click':
                    cursor_controller.click('right')
                elif hand_action == 'drag':
                    if final_pos:
                        cursor_controller.drag_to(final_pos[0], final_pos[1])
                elif hand_action == 'scroll':
                    cursor_controller.scroll(30)
                
            if system_state in ['EYE', 'HYBRID']:
                eye_action = gesture_engine.process_eye_gestures(eye_data, final_pos)
                if eye_action == 'blink_click' or eye_action == 'dwell_click':
                    cursor_controller.click('left')
        
        curr_time = time.time()
        fps = 1 / (max(curr_time - prev_time, 0.001))
        prev_time = curr_time
        
        display_frame = ui_overlay.draw(frame, hand_data, eye_data, active_mode, fps)
        
        # Display system state on UI
        color = (0, 255, 0) if system_state != 'OFF' else (0, 0, 255)
        cv2.putText(display_frame, f"STATE: {system_state}", (20, 160), ui_overlay.font, 1, color, 2)
        cv2.putText(display_frame, "[1]HAND [2]EYE [3]HYBRID [0]OFF", (20, 200), ui_overlay.font, 0.6, (200, 200, 200), 1)
        
        cv2.imshow("Cerberus Future Mouse", display_frame)
            
    cap.release()
    cv2.destroyAllWindows()
    print("System offline.")

if __name__ == "__main__":
    main()
