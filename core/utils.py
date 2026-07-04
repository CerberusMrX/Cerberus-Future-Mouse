import math
import numpy as np

def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def get_angle(p1, p2, p3):
    """
    Calculate the angle at p2 given points p1, p2, and p3.
    """
    a = calculate_distance(p1, p2)
    b = calculate_distance(p2, p3)
    c = calculate_distance(p1, p3)
    
    try:
        angle_rad = math.acos((a**2 + b**2 - c**2) / (2 * a * b))
        return math.degrees(angle_rad)
    except Exception:
        return 0.0

def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))
