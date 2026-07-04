# Hybrid Fusion Algorithm

The Cerberus Future Mouse utilizes a sophisticated hybrid fusion engine designed to combine the speed of hand tracking with the precision of eye tracking.

## Core Logic

The system dynamically shifts priority between hand gestures and eye gaze based on the user's intent, inferred through motion analysis.

1. **Active Hand (Macroscopic Movement)**:
   When the hand's index finger is moving beyond a distance threshold (`STILL_DIST_THRESHOLD`), the engine assumes the user is performing a gross cursor movement.
   - Hand coordinates are assigned a ~95% weight.
   - Eye coordinates are assigned a ~5% weight (or ignored).
   - *Result*: Fast, responsive movement across the screen.

2. **Stationary Hand (Microscopic Adjustment)**:
   When the hand has remained within the stillness threshold for a set number of frames (`HAND_STILL_THRESHOLD`), the engine infers the user has reached their general target area.
   - The engine shifts weights to favor eye gaze for fine-tuning.
   - Hand coordinates receive ~40% weight (acting as an anchor).
   - Eye coordinates receive ~60% weight (driving the micro-adjustment).
   - *Result*: The cursor shifts slightly to land exactly where the user is looking, mimicking "UI snapping".

3. **Smoothing Pipeline**:
   Both raw input streams pass through individual `ExponentialSmoother` objects.
   - The Hand stream uses a faster smoothing factor because MediaPipe Hands is generally stable.
   - The Eye stream uses a slower, heavier smoothing factor to eliminate the natural jitter and saccades of the human eye.
   - Finally, the fused coordinate passes through a third smoother to ensure seamless transitions between HAND and HYBRID modes.
