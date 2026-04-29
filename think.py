import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"

def ask(question: str) -> str:
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": (
                f"You are a helpful assistant for a blind person. "
                f"Answer clearly in 2 to 3 sentences. "
                f"Do not ask follow-up questions: {question}"
            ),
            "stream": False,
        }, timeout=120)
        return response.json().get('response', '').strip()
    except Exception as e:
        print(f"[THINK ERROR]: {e}")
        return ""
