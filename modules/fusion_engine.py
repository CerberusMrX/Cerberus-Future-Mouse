from core.smoothing import ExponentialSmoother, DynamicSmoother
from core.utils import calculate_distance

class FusionEngine:
    """
    Intelligent fusion system:
    - If hand is active -> use hand for movement
    - If hand is still -> use eye for micro-adjustment
    - Blends inputs using confidence scoring
    """
    def __init__(self):
        # Highest Quality Tracking: Heavily tuned smoothing parameters prioritize accuracy and stability
        self.hand_smoother = DynamicSmoother(min_alpha=0.05, max_alpha=0.55, dist_threshold=50.0) 
        self.eye_smoother = DynamicSmoother(min_alpha=0.01, max_alpha=0.3, dist_threshold=10.0) 
        self.final_smoother = ExponentialSmoother(alpha=0.35)
        
        self.prev_hand_pos = None
        self.hand_still_frames = 0
        
        # Thresholds
        self.HAND_STILL_THRESHOLD = 8 # frames to count as still
        self.STILL_DIST_THRESHOLD = 20 # pixels (in screen space) to ignore micro-jitter
        
        self.active_mode = "HAND"
        
    def fuse(self, hand_pos, eye_pos, hand_conf=1.0, eye_conf=1.0):
        """
        hand_pos: (x, y) or None
        eye_pos: (x, y) or None
        Returns: ((x, y), mode_string) final smoothed coordinate and current mode
        """
        # Smooth individual signals first
        smooth_hand = self.hand_smoother.update(hand_pos) if hand_pos else None
        smooth_eye = self.eye_smoother.update(eye_pos) if eye_pos else None
        
        # State detection
        is_hand_still = False
        if smooth_hand:
            if self.prev_hand_pos:
                dist = calculate_distance(self.prev_hand_pos, smooth_hand)
                if dist < self.STILL_DIST_THRESHOLD:
                    self.hand_still_frames += 1
                else:
                    self.hand_still_frames = 0
            self.prev_hand_pos = tuple(smooth_hand)
            
            if self.hand_still_frames > self.HAND_STILL_THRESHOLD:
                is_hand_still = True

        # Decision making
        if smooth_hand and not smooth_eye:
            final_pos = smooth_hand
            self.active_mode = "HAND"
        elif smooth_eye and not smooth_hand:
            final_pos = smooth_eye
            self.active_mode = "EYE"
        elif smooth_hand and smooth_eye:
            if is_hand_still:
                # Hand is still, use eye for micro-adjustment around the hand's resting point
                # We blend a little bit of eye to shift the hand focus
                weight_hand = 0.4
                weight_eye = 0.6
                self.active_mode = "HYBRID (EYE FOCUS)"
            else:
                # Hand is moving, trust hand mostly
                weight_hand = 0.95
                weight_eye = 0.05
                self.active_mode = "HYBRID (HAND FOCUS)"
                
            # Apply confidence
            total_weight = (weight_hand * hand_conf) + (weight_eye * eye_conf)
            if total_weight == 0:
                final_pos = smooth_hand # Fallback
            else:
                norm_hand_w = (weight_hand * hand_conf) / total_weight
                norm_eye_w = (weight_eye * eye_conf) / total_weight
                
                final_x = norm_hand_w * smooth_hand[0] + norm_eye_w * smooth_eye[0]
                final_y = norm_hand_w * smooth_hand[1] + norm_eye_w * smooth_eye[1]
                final_pos = (final_x, final_y)
        else:
            self.active_mode = "NONE"
            return None, self.active_mode
            
        final_smoothed = self.final_smoother.update(final_pos)
        return (int(final_smoothed[0]), int(final_smoothed[1])), self.active_mode
