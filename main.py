import time
import sys
import os
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from speak import speak
from listen import listen_for_command
from ocr import capture_image
from vision import analyze_image
from think import ask

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"

def needs_camera(command: str) -> bool:
    """Ask the LLM if this question requires seeing an image."""
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": (
                f"Does this question require looking at a camera image to answer? "
                f"Answer only YES or NO.\n"
                f"Question: '{command}'"
            ),
            "stream": False,
        }, timeout=15)
        answer = r.json().get('response', '').strip().upper()
        print(f"[CAMERA NEEDED]: {answer}")
        return "YES" in answer
    except:
        # Fallback to simple phrase matching if LLM fails
        phrases = ["what do you see", "what is in front", "read this",
                   "describe", "what am i holding", "what is this",
                   "what does this say", "look at", "wearing",
                   "holding", "in front of you"]
        return any(p in command.lower() for p in phrases)

def warmup():
    print("[WARMUP]: Loading gemma3:4b into GPU...")
    t0 = time.time()
    try:
        requests.post(OLLAMA_URL, json={
            "model": MODEL, "prompt": "hi", "stream": False,
        }, timeout=60)
        print(f"[WARMUP]: Ready in {time.time()-t0:.1f}s")
    except Exception as e:
        print(f"[WARMUP]: Warning - {e}")

def handle_command(command: str):
    if not command or len(command) < 2:
        speak("I did not catch that. Please try again.")
        return
    print(f"\n[COMMAND]: {command}")
    if needs_camera(command):
        speak("Let me take a look.")
        frame, img_path = capture_image()
        if img_path:
            response = analyze_image(img_path, command)
        else:
            response = "I could not access the camera."
    else:
        response = ask(command)
    if not response:
        speak("I could not process that. Please try again.")
        return
    print(f"[RESPONSE]: {response}")
    speak(response)

def main():
    print("[STARTUP]: Blind assistant starting...")
    warmup()
    print("[INFO]: Say 'exit' or press Ctrl+C to stop")
    print("-"*50)
    speak("Blind assistant is ready. Speak your command.")
    while True:
        try:
            command = listen_for_command(duration=5)
            if not command.strip():
                continue
            if any(w in command.lower() for w in ["exit","quit","stop","goodbye"]):
                speak("Goodbye.")
                break
            handle_command(command)
            time.sleep(0.3)
        except KeyboardInterrupt:
            speak("Shutting down.")
            break
        except Exception as e:
            print(f"[ERROR]: {e}")
            speak("Something went wrong. Please try again.")

if __name__ == "__main__":
    main()
