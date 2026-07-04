import math
from core.utils import calculate_distance

class ExponentialSmoother:
    def __init__(self, alpha=0.5):
        """
        alpha: Smoothing factor between 0 and 1.
        1 means no smoothing (fastest, most jittery).
        0 means infinite smoothing (frozen).
        """
        self.alpha = alpha
        self.value = None
        
    def update(self, new_value):
        if self.value is None:
            self.value = list(new_value)
        else:
            self.value = [
                self.alpha * new_value[i] + (1 - self.alpha) * self.value[i]
                for i in range(len(new_value))
            ]
        return self.value
        
    def reset(self):
        self.value = None

class DynamicSmoother:
    def __init__(self, min_alpha=0.1, max_alpha=0.9, dist_threshold=50.0):
        self.min_alpha = min_alpha
        self.max_alpha = max_alpha
        self.dist_threshold = dist_threshold
        self.value = None
        
    def update(self, new_value):
        if self.value is None:
            self.value = list(new_value)
            return self.value
            
        dist = calculate_distance(self.value, new_value)
        
        # Scale alpha based on movement speed. 
        # Fast movement = high alpha (0 lag). Slow movement = low alpha (perfect lock).
        factor = min(1.0, dist / self.dist_threshold)
        alpha = self.min_alpha + factor * (self.max_alpha - self.min_alpha)
        
        self.value = [
            alpha * new_value[i] + (1 - alpha) * self.value[i]
            for i in range(len(new_value))
        ]
        return self.value
