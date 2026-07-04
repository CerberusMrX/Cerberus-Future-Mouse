import pyautogui

class Config:
    # Camera settings
    CAMERA_ID = 0
    FRAME_WIDTH = 1280
    FRAME_HEIGHT = 720
    FPS = 30
    
    # Hand Tracking
    HAND_MIN_DETECTION_CONFIDENCE = 0.85
    HAND_MIN_TRACKING_CONFIDENCE = 0.85
    
    # Eye Tracking
    FACE_MIN_DETECTION_CONFIDENCE = 0.7
    FACE_MIN_TRACKING_CONFIDENCE = 0.7
    
    # Screen and Cursor
    # Automatically get screen size
    try:
        SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
    except Exception:
        SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
        
    # Moderated alpha to heavily prioritize accuracy and reduce cursor jitter
    CURSOR_SMOOTHING = 0.20
    
    # Gestures
    PINCH_THRESHOLD = 35 # pixel distance between thumb and index
    DRAG_HOLD_FRAMES = 10 # frames to hold pinch to start drag
    BLINK_THRESHOLD = 0.23 # Increased so blinks trigger easier
    DWELL_FRAMES = 20 # Reduced frames (less than 1 sec to auto-click by staring)
