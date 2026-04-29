# Blind Assistant — Jetson Orin Nano

An AI-powered blind assistant that runs fully offline on the NVIDIA Jetson Orin Nano. It listens to voice commands, captures camera images, describes scenes, reads text, and speaks responses aloud.

## Demo
The system responds to natural voice commands like:
- "What do you see in front of you?"
- "What does this label say?"
- "What is the man wearing?"
- "What is ibuprofen used for?"

## Hardware Required
- NVIDIA Jetson Orin Nano (8GB)
- USB webcam
- USB headset (microphone + speaker)

## Models Used
| Model | Size | Role | Hardware |
|-------|------|------|----------|
| gemma3:4b | 3.3GB | Vision + OCR + Text QA | GPU via Ollama |
| Whisper small | 500MB | Speech to text | CPU |
| espeak-ng | ~4MB | Text to speech | CPU |

## Pipeline

Voice command (mic)
→
Whisper small (speech → text) [CPU]
→
gemma3:4b: "Does this need a camera?" [GPU]
→
YES → Camera capture → gemma3:4b vision query [GPU]
NO  → gemma3:4b text query [GPU]
→
espeak-ng (text → speech) [CPU]
→
USB headset speaker

## Setup Instructions

### 1. Prerequisites
- NVIDIA Jetson Orin Nano with L4T 36.x
- Python 3.10
- CUDA 12.6

### 2. Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma3:4b
```

### 3. Clone this repository
```bash
git clone https://github.com/hac25-aub/blind-assistant-jetson.git
cd blind-assistant-jetson
```

### 4. Create virtual environment and install dependencies
```bash
python3 -m venv blind_assistant_env
source blind_assistant_env/bin/activate
pip install -r requirements.txt
```

### 5. Install system dependencies
```bash
sudo apt install -y espeak-ng sox tesseract-ocr
```

### 6. Set maximum performance
```bash
sudo jetson_clocks
```

### 7. Run
```bash
python3 main.py
```

## File Structure
| File | Role |
|------|------|
| main.py | Entry point — orchestrates everything |
| listen.py | Records audio + Whisper transcription |
| vision.py | Image analysis via gemma3:4b |
| think.py | Text questions via gemma3:4b |
| ocr.py | Camera capture via OpenCV |
| speak.py | Text to speech via espeak-ng |
| config.py | Shared settings and paths |

## Notes
- GPU (gemma3) and CPU (Whisper) run on separate hardware due to Jetson NvMap memory constraint
- Model warmup happens at startup (~60s first boot, ~5s if recently used)
- USB headset device is auto-detected by name on every boot
- Tested on L4T R36.4.7, CUDA 12.6, Ollama 0.20.5

## Course
EECE490 — American University of Beirut, 2026
