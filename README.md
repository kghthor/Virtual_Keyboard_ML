markdown
# 👆 AI Virtual Keyboard with Hand Tracking



An innovative virtual keyboard that uses computer vision to detect finger movements and simulate keyboard inputs. Control your computer hands-free using just your webcam!

## ✨ Features

- **Touchless Typing**: Type by touching your index finger to thumb over virtual keys
- **Ultra-Blur Background**: Focuses attention on keyboard and hand landmarks
- **Full Keyboard Layout**: Includes alphanumeric keys, space, enter, backspace, and shift
- **Visual Feedback**: Highlights pressed keys and shows typed text
- **Caps Lock Indicator**: Visual cue for uppercase/lowercase mode
- **Optimized Detection**: Only registers intentional index-thumb touches

## 🛠️ Technologies Used

- **MediaPipe** - For real-time hand tracking and landmark detection
- **OpenCV** - For camera input processing and visual interface
- **PyAutoGUI** - For simulating keyboard inputs
- **NumPy** - For image processing and mask operations

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-virtual-keyboard.git
   cd ai-virtual-keyboard
Install dependencies:

bash
pip install -r requirements.txt
(Create requirements.txt with: opencv-python, mediapipe, pyautogui, numpy)

Run the application:

bash
python virtual_keyboard.py
🎮 How to Use
Position your hands in view of the webcam

Move your index finger to hover over keys

Touch your index finger to thumb to "press" a key

Use special keys:

Shift: Toggle caps lock

Space: Insert space

Enter: New line

Backspace: Delete last character

🖼️ Interface Overview


Hand Landmarks: Visual tracking of fingers and joints

Virtual Keyboard: On-screen keyboard layout

Text Display: Shows typed characters in real-time

Caps Lock Indicator: Shows current case mode

⚙️ Technical Details
The system works by:

Detecting hand landmarks using MediaPipe

Calculating distance between index finger (Landmark 8) and thumb (Landmark 4)

Registering key presses only when distance < threshold (0.03)

Applying Gaussian blur to all non-essential areas

Simulating keyboard presses with PyAutoGUI

🤝 Contributing
Contributions are welcome! Please open an issue or PR for:

Bug fixes

New features

Performance improvements

Better documentation

📜 License
MIT License - Free for personal and commercial use
