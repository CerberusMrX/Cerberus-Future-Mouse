# Cerberus Future Mouse Setup Guide

## Requirements
- Python 3.9+
- A working webcam

## Installation

1. Clone or download this repository.
2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # or
   venv\Scripts\activate     # On Windows
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the System
```bash
python main.py
```

## Troubleshooting
- **Linux Users**: If you encounter issues with `pyautogui`, you might need to install `scrot` or `python3-tk` depending on your desktop environment.
  ```bash
  sudo apt-get install python3-tk python3-dev
  ```
- **Wayland**: PyAutoGUI may have issues on Wayland. If the mouse does not move, consider switching to X11 or using a specific backend tool for Wayland (like `ydotool`).
- **Camera Access**: If the camera fails to open, ensure you have given Python permission to access your webcam. Check if `/dev/video0` is available on Linux.
