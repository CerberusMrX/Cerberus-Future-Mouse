# Optimization Techniques

To achieve real-time performance (≥ 24 FPS) while running complex ML models simultaneously, several optimizations are applied:

1. **Lightweight Model Layers**:
   - MediaPipe is utilized due to its highly optimized C++ backend and efficient graph execution.
   - We extract only the necessary landmarks (e.g., fingertips rather than all 21 hand joints) during the logic phase.

2. **Decoupled Smoothing**:
   - Instead of running a computationally heavy full Kalman Filter matrix for every coordinate, we use mathematically simplified Exponential Smoothing. This uses $O(1)$ memory and CPU cycles per frame while providing 90% of the benefit of a Kalman filter.

3. **Deadzone Camera Mapping**:
   - `map_camera_to_screen` utilizes boundary padding (deadzones). This prevents the user from having to reach the absolute edge of the camera's FOV to reach the edge of their monitor, reducing physical fatigue and tracking loss at the frame edges.

4. **Future Multi-threading Capability**:
   - The architecture is strictly decoupled into `EyeTracker`, `HandTracker`, and `FusionEngine`. For ultra-low latency, the capture loop can be separated into a distinct daemon thread using Python `threading` or `multiprocessing` queues.

5. **Resource Bounding**:
   - Limit `max_num_hands=1` and `max_num_faces=1` in MediaPipe configurations. The tracking algorithm immediately ignores background noise once the primary target is locked.
