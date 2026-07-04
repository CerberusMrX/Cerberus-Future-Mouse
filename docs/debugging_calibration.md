# Debugging & Calibration Guide

## Auto-Calibration Process
When the software starts, you will see a prominent red text: 
`CALIBRATING... LOOK AT THE CENTER OF THE SCREEN`
You must look directly at the center of your monitor for approximately 2-3 seconds.
During this phase, the `AutoCalibrator` collects your raw iris coordinates to establish a "Neutral Gaze Vector." 

### Why is this needed?
Every user sits at a different height, angle, and distance from their webcam. Without calibration, the system wouldn't know if looking at pixels `(600, 400)` means you are looking left, right, or center. The offset calculation requires this baseline.

## Debugging Common Issues

1. **Cursor is too jumpy / jittery**
   - *Fix*: Open `core/config.py` and lower `CURSOR_SMOOTHING` (e.g., from `0.2` to `0.1`). A lower value increases smoothing but adds slight latency.

2. **Eye tracking cannot reach the edge of the screen**
   - *Fix*: In `main.py`, within the eye tracking section, increase the `sensitivity` multiplier (e.g., from `5.0` to `7.0`).

3. **Hand gestures aren't firing (Pinch/Scroll)**
   - *Fix*: Open `core/config.py` and increase `PINCH_THRESHOLD`. Some users have larger hands, causing fingertips to appear further apart in pixel-space even when pinched.

4. **Accidental clicks happening too often**
   - *Fix*: Open `core/config.py` and increase `DRAG_HOLD_FRAMES`. This forces you to hold the pinch longer before it registers.

5. **Camera isn't opening**
   - *Fix*: Check `CAMERA_ID` in `config.py`. Usually, `0` is the default laptop webcam. If you have an external USB webcam, it might be `1` or `2`.
