import time
from core.config import Config
from core.utils import calculate_distance

class GestureEngine:
    def __init__(self):
        self.pinch_start_frame = 0
        self.is_dragging = False
        self.was_dragging = False
        
        self.last_blink_time = 0
        self.blink_debounce = 0.5 # seconds
        
        self.dwell_start_time = 0
        self.last_gaze_pos = None
        self.dwell_radius_threshold = 20 # pixels
        
        self.scroll_start_y = None
        
    def process_hand_gestures(self, hand_data):
        """
        Process hand gestures based on landmarks.
        Returns the action string or None.
        """
        if not hand_data:
            self.is_dragging = False
            self.pinch_start_frame = 0
            self.scroll_start_y = None
            if self.was_dragging:
                self.was_dragging = False
                return 'release'
            return None
            
        thumb = hand_data['thumb_tip']
        index = hand_data['index_tip']
        middle = hand_data['middle_tip']
        
        if not thumb or not index or not middle:
            return None
            
        dist_thumb_index = calculate_distance(thumb, index)
        dist_thumb_middle = calculate_distance(thumb, middle)
        dist_index_middle = calculate_distance(index, middle)
        
        # Pinch -> Left Click or Drag
        if dist_thumb_index < Config.PINCH_THRESHOLD:
            self.pinch_start_frame += 1
            if self.pinch_start_frame > Config.DRAG_HOLD_FRAMES:
                self.is_dragging = True
                self.was_dragging = True
                return 'drag'
            else:
                return None # Wait to see if it's a click or drag
        else:
            if 0 < self.pinch_start_frame <= Config.DRAG_HOLD_FRAMES:
                # Released quickly -> Click
                self.pinch_start_frame = 0
                self.is_dragging = False
                self.was_dragging = False
                return 'left_click'
            
            self.pinch_start_frame = 0
            self.is_dragging = False
            
            if self.was_dragging: # Was dragging, now released
                self.was_dragging = False
                return 'release'
            
        # Index + middle pinch -> right click (Interpreter as thumb touching middle)
        if dist_thumb_middle < Config.PINCH_THRESHOLD:
            # We can use a debounce here if needed, but for now simple return
            return 'right_click'
            
        # Two fingers up -> scroll mode
        # If index and middle are close to each other, but far from thumb
        if dist_index_middle < Config.PINCH_THRESHOLD * 1.5 and dist_thumb_index > Config.PINCH_THRESHOLD * 2:
            return 'scroll'
            
        return None

    def process_eye_gestures(self, eye_data, cursor_pos):
        """
        Process eye gestures like blink and dwell.
        """
        if not eye_data:
            return None
            
        current_time = time.time()
        
        # Blink -> Click Fallback
        if eye_data['is_blinking']:
            if current_time - self.last_blink_time > self.blink_debounce:
                self.last_blink_time = current_time
                return 'blink_click'
                
        # Dwell click
        if cursor_pos:
            if not self.last_gaze_pos:
                self.last_gaze_pos = cursor_pos
                self.dwell_start_time = current_time
            else:
                dist = calculate_distance(self.last_gaze_pos, cursor_pos)
                if dist < self.dwell_radius_threshold:
                    dwell_seconds = Config.DWELL_FRAMES / Config.FPS
                    if current_time - self.dwell_start_time > dwell_seconds:
                        self.dwell_start_time = current_time # Reset
                        return 'dwell_click'
                else:
                    self.last_gaze_pos = cursor_pos
                    self.dwell_start_time = current_time
                    
        return None
