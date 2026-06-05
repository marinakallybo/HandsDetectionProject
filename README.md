# 🖐 HandsDetectionProject

🇧🇷 [Versão em Português](README.pt.md)

Control your computer using only hand gestures — no mouse needed. This project uses computer vision to detect hand landmarks in real time and translate them into mouse movements, clicks, scrolling, and even drawing.

> Built with MediaPipe, OpenCV, and PyAutoGUI.

---

<!-- Add a demo gif here after recording -->
<!-- ![Demo](assets/demo.gif) -->

---

## ✨ Features

- **Mouse control** — move the cursor using your index finger
- **Click** — pinch gesture (thumb + index finger)
- **Scroll** — raise index and middle fingers, move hand up/down
- **Paint mode** — toggle with `P`; raise index finger to draw, pinch to click
- **Smooth movement** — exponential moving average (EMA) to reduce cursor tremor
- **Cursor freeze** — cursor locks in place while pinch gesture is forming, preventing misclicks
- **HUD overlay** — live mode indicator and pinch progress bar on the camera feed

---

## 🗂 Project Structure

```
HandsDetectionProject/
├── main.py                 # Entry point and main loop
├── detector_maos.py        # Hand detection, landmark drawing, and HUD
├── controlador_mouse.py    # Mouse control, scroll, click, and paint logic
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

| Gesture | Mode | Action |
|---|---|---|
| Index finger up | Mouse | Move cursor |
| Thumb + index pinch | Mouse | Left click |
| Index + middle fingers up | Mouse | Scroll mode |
| Hand up (scroll mode) | Mouse | Scroll up |
| Hand down (scroll mode) | Mouse | Scroll down |
| Press `P` | — | Toggle paint mode |
| Index finger up | Paint | Draw |
| Thumb + index pinch | Paint | Left click |
| Lower index finger | Paint | Stop drawing |

---

## ⚙️ Configuration

You can tweak the controller parameters in `main.py`:

```python
controlador = ControladorMouse(
    largura_cam,
    altura_cam,
    margem=100,       # Active zone margin in pixels (excludes camera edges)
    limiar_pinca=47,  # Pinch distance threshold in pixels
)
```

And the smoothing factor in `controlador_mouse.py`:

```python
self.alpha = 0.17   # Mouse mode: lower = smoother but slower (range: 0.1 – 0.4)
self.alpha = 0.55   # Paint mode: higher = more responsive for drawing
```

---

## 🛠 Tech Stack

- [MediaPipe](https://mediapipe.dev/) — hand landmark detection
- [OpenCV](https://opencv.org/) — video capture and image drawing
- [PyAutoGUI](https://pyautogui.readthedocs.io/) — mouse control

---

## 📄 License

MIT License. Feel free to use, modify, and distribute.
