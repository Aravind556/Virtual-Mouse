# AI Virtual Mouse

> Control your computer using hand gestures, without touching any physical device.

## ✨ Features

- **Touchless Control** — Navigate your computer using only hand gestures
- **Precision Movement** — Smooth cursor tracking follows your index finger
- **Natural Gestures** — Click by pinching, scroll by positioning your thumb
- **Visual Feedback** — On-screen indicators show detected gestures and actions
- **Customizable** — Adjustable sensitivity and response parameters

## 🔧 Requirements

- Python 3.7-3.9 (recommended for best compatibility)
- Webcam
- Libraries: OpenCV, MediaPipe, NumPy, PyAutoGUI

## 🚀 Installation

1. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python AIVirtualMouse.py
   ```

## 🖐 Gesture Controls

| Gesture | Action | Indicator |
|:-------:|:-------|:----------|
| ![Index Up](https://i.imgur.com/index.png) | **Move Cursor** — Index finger up | Purple circle |
| ![Pinch](https://i.imgur.com/pinch.png) | **Click** — Index and middle finger pinched | Green circle |
| ![Thumb Up](https://i.imgur.com/thumb-up.png) | **Scroll Up** — Thumb above center line | Green up arrow |
| ![Thumb Down](https://i.imgur.com/thumb-down.png) | **Scroll Down** — Thumb below center line | Green down arrow |

## ⚙️ Configuration

Adjust these parameters in `AIVirtualMouse.py` to customize the experience:

```python
frameR = 100          # Border size (smaller = more precision)
smoothening = 7       # Mouse smoothness (higher = smoother)
scroll_sensitivity = 5 # Scroll speed multiplier
scroll_threshold = 20  # Dead zone for scroll detection
```

## 🔍 Troubleshooting

- **No response?** Ensure good lighting and position your hand within camera view
- **Erratic cursor?** Increase smoothening value in settings
- **Exit program** — Press 'q' key while window is active

## 💡 How It Works

The system uses MediaPipe's hand tracking to detect 21 landmarks on your hand. These landmarks determine finger positions, which are then mapped to cursor coordinates and gestures using OpenCV and PyAutoGUI.

## 📄 License

MIT License

---

*Created with computer vision and hand tracking technology*


