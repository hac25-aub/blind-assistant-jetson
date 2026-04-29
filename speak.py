import subprocess

def speak(text: str):
    print(f"[ASSISTANT]: {text}")
    try:
        # espeak-ng can output directly to pulse
        subprocess.run([
            "espeak-ng",
            "-s", "140",
            "-p", "50",
            "-a", "180",
            text
        ])
    except Exception as e:
        print(f"[SPEAK ERROR]: {e}")
