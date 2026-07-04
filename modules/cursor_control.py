import pyautogui
from core.config import Config
from core.utils import clamp

class CursorController:
    def __init__(self):
        # We disable failsafe locally so intentional edge movements are allowed,
        # but the main program should provide a kill switch (e.g., press 'q')
        pyautogui.FAILSAFE = False 
        
        self.screen_width = Config.SCREEN_WIDTH
        self.screen_height = Config.SCREEN_HEIGHT
        
        # Smoothing variables
        self.prev_x = 0
        self.prev_y = 0
        
    def move_to(self, x, y):
        """Move cursor to absolute screen coordinates."""
        cx = clamp(x, 0, self.screen_width - 1)
        cy = clamp(y, 0, self.screen_height - 1)
        
        try:
            pyautogui.moveTo(cx, cy, _pause=False)
        except Exception as e:
            print(f"Cursor move error: {e}")
            
    def click(self, button='left'):
        try:
            pyautogui.click(button=button, _pause=False)
        except Exception as e:
            print(f"Click error: {e}")
            
    def double_click(self, button='left'):
        try:
            pyautogui.doubleClick(button=button, _pause=False)
        except Exception as e:
            print(f"Double Click error: {e}")
            
    def drag_to(self, x, y):
        cx = clamp(x, 0, self.screen_width - 1)
        cy = clamp(y, 0, self.screen_height - 1)
        try:
            pyautogui.dragTo(cx, cy, button='left', _pause=False)
        except Exception as e:
            print(f"Drag error: {e}")
            
    def scroll(self, amount):
        try:
            pyautogui.scroll(amount, _pause=False)
        except Exception as e:
            print(f"Scroll error: {e}")

    def map_camera_to_screen(self, cam_x, cam_y, cam_w, cam_h, deadzone=100):
        """
        Map camera coordinates to screen coordinates.
        Uses a deadzone around the camera frame edges for easier edge access.
        """
        # Active area within the camera frame
        active_w = cam_w - 2 * deadzone
        active_h = cam_h - 2 * deadzone
        
        # Calculate percentage position within active area
        pct_x = (cam_x - deadzone) / active_w
        pct_y = (cam_y - deadzone) / active_h
        
        # Clamp percentages to 0-1
        pct_x = clamp(pct_x, 0.0, 1.0)
        pct_y = clamp(pct_y, 0.0, 1.0)
        
        # We don't need to mirror X axis here because the frame is already flipped in main.py
        
        screen_x = int(pct_x * self.screen_width)
        screen_y = int(pct_y * self.screen_height)
        
        return screen_x, screen_y
