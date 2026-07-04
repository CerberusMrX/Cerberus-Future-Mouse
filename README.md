<div align="center">
  
# 🖱️ Cerberus Future Mouse

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange.svg)](https://developers.google.com/mediapipe)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A next-generation, production-grade hybrid control system combining hand gesture tracking and eye gaze tracking to create a completely hands-free and touchless mouse replacement using a standard webcam.**

Authored by **Sudeepa Wanigarathna**

<br/>


</div>

## ✨ Features

- 🖐️ **Primary Control (Hand Tracking)**
  - **Point:** Move the cursor naturally using your index finger.
  - **Pinch:** Execute left-clicks with a thumb-index pinch gesture.
  - **Scroll:** Scroll smoothly using a two-finger gesture.
  - **Drag & Drop:** Maintain a pinch while moving to drag elements across the screen.

- 👁️ **Precision Layer (Eye Tracking)**
  - **Gaze Movement:** Micro-adjustments and UI element snapping using precise eye gaze direction.
  - **Blink to Click:** Execute rapid left-clicks simply by blinking.
  - **Dwell Click:** Stare at a specific spot for >0.5 seconds for automatic clicking.

- 🧠 **Hybrid Fusion Engine**
  - Intelligently blends hand and eye tracking data for the ultimate combination of macro-speed and micro-precision.
  - Dynamically adjusts to the confidence levels of the MediaPipe models.

- ⚙️ **Auto-Calibration**
  - Instantly adapts to your room's lighting conditions.
  - Accounts for camera geometry, positioning, and individual user physical traits without tedious manual setup.

---

## 🛠️ Technology Stack

Powered by modern Computer Vision and Machine Learning tools:
- **Python 3.8+**
- **OpenCV (`opencv-python`)**: For high-performance video capture and image processing.
- **Google MediaPipe**: State-of-the-art ML models for robust face and hand landmark detection.
- **PyAutoGUI**: Cross-platform OS-level cursor manipulation and clicking.
- **NumPy & SciPy**: Advanced mathematics for spatial calculations.
- **FilterPy**: Kalman filtering for silky-smooth cursor stabilization.

---

## 🏗️ System Architecture

The project is heavily modularized for scalability and easy maintenance:

- `main.py` - Application entry point and core loop.
- `core/config.py` - Global constants and configuration parameters.
- `modules/`
  - `auto_calibration.py` - Handles initialization and user calibration.
  - `hand_tracking.py` - MediaPipe Hand Landmarker integration.
  - `eye_tracking.py` - MediaPipe Face Landmarker (Iris) integration.
  - `fusion_engine.py` - Logic to merge eye and hand data vectors.
  - `gesture_engine.py` - Interprets physical movements into logical OS actions.
  - `cursor_control.py` - Interfacing with `pyautogui` for screen control.
  - `ui_overlay.py` - OpenCV-based Heads-Up Display (HUD) rendering.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8 or higher installed. A dedicated GPU is recommended but not strictly required as MediaPipe is highly optimized.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cerberusmrx/cerberus-future-mouse.git
   cd cerberus-future-mouse
   ```

2. **Create a virtual environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Model Files:**
   Ensure the MediaPipe task models (`face_landmarker.task`, `hand_landmarker.task`) are present in the root directory.

### Usage

Start the system by running the main execution file:
```bash
python main.py
```

Upon launching, the system will start in the **OFF** state. Use the following keyboard controls to navigate modes:

#### ⌨️ Keyboard Controls
- `[1]` - **HAND Only Mode**
- `[2]` - **EYE Only Mode**
- `[3]` - **HYBRID Mode** (Eye & Hand Fusion)
- `[0]` - **Turn OFF**
- `[Q]` or `[ESC]` - **Exit Application**

#### 🎮 On-Screen Interactions
- **Eye Mode / Hybrid Mode:** 
  - Look around to move the cursor. 
  - **Blink** to left-click. 
  - **Stare** at one spot for 0.5s to trigger an auto-click.
- **Hand Mode / Hybrid Mode:** 
  - Point index finger to move. 
  - Pinch index and thumb to click/drag. 
  - Two fingers up to scroll.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <i>"The best way to predict the future is to invent it."</i>
</div>
