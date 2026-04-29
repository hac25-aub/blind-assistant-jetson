import requests
import base64

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"

def analyze_image(image_path: str, user_question: str) -> str:
    try:
        with open(image_path, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode()

        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": (
                f"You are a vision assistant helping a blind person. "
                f"Look at this image and answer this specific question: '{user_question}'. "
                f"Answer the question directly and concisely in 2-3 sentences. "
                f"Only mention what is relevant to the question. "
                f"Do not give a general scene description unless asked. "
                f"Do not ask follow-up questions."
            ),
            "stream": False,
            "images": [img_b64]
        }, timeout=120)
        return response.json().get('response', '').strip()
    except Exception as e:
        print(f"[VISION ERROR]: {e}")
        return ""
