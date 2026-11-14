# 🚗 Quick Start Guide - Driver Drowsiness Detection System with Continuous Alert

## ✅ Installation Complete!

Your Driver Drowsiness Detection System with **continuous alert sound** is ready to use.

## 🚀 How to Run

### Option 1: Using VS Code Task (Easiest)
1. Press `Ctrl+Shift+B` (or Cmd+Shift+B on Mac)
2. Select "Start Drowsiness Detection"
3. Press Enter

### Option 2: Terminal Command
```bash
python drowsiness_detector.py
```

## 📋 What You'll See

Once running:
- **Webcam feed** with face and eye detection boxes
- **EAR (Eye Aspect Ratio)** display - lower values = eyes closing
- **Alert message** - appears when drowsiness detected
- **Alert sound** - plays automatically (if available)

## ⚙️ Controls

| Key | Action |
|-----|--------|
| **Q** | Quit the application |

## 🎯 Tips for Best Results

1. **Lighting**: Ensure good lighting on your face
2. **Camera Position**: Place camera at eye level, 1-2 feet away
3. **Sensitivity**: Adjust thresholds in `drowsiness_detector.py` if needed:
   - `EYE_AR_THRESH`: Lower = more sensitive (default: 0.2)
   - `EYE_AR_CONSEC_FRAMES`: Lower = faster alerts (default: 30)

## 🔧 Configuration

Edit these values in `drowsiness_detector.py`:

```python
self.EYE_AR_THRESH = 0.2              # Eye closure sensitivity
self.EYE_AR_CONSEC_FRAMES = 30        # Frames before alert
```

## 🎵 Alert System

**Continuous Alert Sound** - The system plays a looping alert sound while drowsiness is detected:
- Beeps continuously in 300ms pulses with pauses
- Auto-stops completely when you open your eyes
- Falls back to system beep on Windows/Mac/Linux
- Place custom `alert.wav` to use your own sound

To generate/regenerate the alert sound:
```bash
python generate_alert.py
```

The alert is a pulsing beep pattern that repeats automatically until eyes are detected open again.

## 📊 How It Detects Drowsiness

```
1. Detect face in video
   ↓
2. Locate both eyes
   ↓
3. Calculate Eye Aspect Ratio (EAR)
   ↓
4. If EAR < 0.2 for 30+ frames
   ↓
5. 🔔 ALERT! Play alarm sound
```

## ⚠️ Important Notes

- This is an **educational prototype** - not a production safety system
- Always practice safe driving habits
- Don't rely solely on this for safety - stay alert!
- For production use, consult professional drowsiness detection solutions

## 🐛 Troubleshooting

### Camera not detected?
- Ensure camera is connected and enabled
- Check if another app is using the camera
- Try changing `camera_index` in code (0, 1, 2, etc.)

### No alert sound?
- Ensure `alert.wav` exists: `python generate_alert.py`
- Check system volume
- On Windows, the system beep is the fallback

### Poor detection?
- Improve lighting
- Clean camera lens
- Adjust `EYE_AR_THRESH` value (try 0.15-0.25)

## 📦 Files in This Project

| File | Purpose |
|------|---------|
| `drowsiness_detector.py` | Main detection system |
| `generate_alert.py` | Creates alert.wav |
| `alert.wav` | Alert sound |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |

## 🎓 Learn More

See `README.md` for:
- Detailed feature explanations
- Advanced configuration
- dlib installation instructions
- Performance optimization tips

---

**Enjoy safe driving! Stay alert! 👀**
