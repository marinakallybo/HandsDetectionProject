# 🖐 HandsDetectionProject

🇧🇷 [Versão em Português](README.pt-br.md)

Control your computer using only hand gestures — no mouse needed. This project uses computer vision to detect hand landmarks in real time and translate them into mouse movements, clicks, and scrolling.

> Built with MediaPipe, OpenCV, and PyAutoGUI.

---

<!-- Add a demo gif here after recording -->
<!-- ![Demo](assets/demo.gif) -->

---

## ✨ Features

- **Mouse control** — move the cursor using your index finger
- **Click** — pinch gesture (thumb + index finger)
- **Scroll** — raise index and middle fingers, move hand up/down
- **Smooth movement** — exponential moving average (EMA) to reduce cursor tremor
- **Cursor freeze** — cursor locks in place while pinch gesture is forming, preventing misclicks
- **HUD overlay** — live mode indicator and pinch progress bar on the camera feed

---

## 🗂 Project Structure

```
HandsDetectionProject/
├── main.py                 # Entry point
├── detector_maos.py        # Hand detection and drawing logic
├── controlador_mouse.py    # Mouse control logic
├── requirements.txt
├── README.md
├── README.pt-br.md
├── models/
│    └── hand_landmarker.task   # Auto-downloaded on first run
└── assets/
     ├── demo.gif
     └── screenshot.png
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/HandsDetectionProject.git
cd HandsDetectionProject
```

### 2. Create and activate a virtual environment
```bash
python -m venv myvenv

# Windows
myvenv\Scripts\activate

# macOS/Linux
source myvenv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run
```bash
python main.py
```

> The MediaPipe hand landmark model (~9MB) will be downloaded automatically on the first run.

---

## 🤚 Gesture Reference

| Gesture | Action |
|---|---|
| Index finger up | Move cursor |
| Thumb + index pinch | Left click |
| Index + middle fingers up | Scroll mode |
| Hand up (scroll mode) | Scroll up |
| Hand down (scroll mode) | Scroll down |

---

## ⚙️ Configuration

You can tweak the controller parameters in `main.py`:

```python
controlador = ControladorMouse(
    largura_cam,
    altura_cam,
    margem=100,       # Active zone margin in pixels (excludes camera edges)
    limiar_pinca=40,  # Pinch distance threshold in pixels
)
```

And the smoothing factor in `controlador_mouse.py`:

```python
self.alpha = 0.17  # Lower = smoother but slower (range: 0.1 – 0.4)
```

---

## 🛠 Tech Stack

- [MediaPipe](https://mediapipe.dev/) — hand landmark detection
- [OpenCV](https://opencv.org/) — video capture and image drawing
- [PyAutoGUI](https://pyautogui.readthedocs.io/) — mouse control

---

## 📄 License

MIT License. Feel free to use, modify, and distribute.
