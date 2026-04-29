import whisper
import sounddevice as sd
import numpy as np
import tempfile
import warnings
import scipy.io.wavfile as wav
import scipy.signal

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

SAMPLE_RATE_WHISPER = 16000

def find_mic():
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if 'AB13X' in d['name'] and d['max_input_channels'] > 0:
            rate = int(d['default_samplerate'])
            print(f"[LISTEN] Found mic: Device {i} — {d['name']} at {rate}Hz")
            return i, rate
    print("[LISTEN] AB13X not found, using default")
    return None, 16000

print("[LISTEN] Loading Whisper small on CPU...")
_model = whisper.load_model("small")
MIC_DEVICE, SAMPLE_RATE_DEVICE = find_mic()
print(f"[LISTEN] Whisper ready | Device {MIC_DEVICE} at {SAMPLE_RATE_DEVICE}Hz")

def listen_for_command(duration=5) -> str:
    print(f"\n[LISTEN] Listening for {duration} seconds...")
    audio = sd.rec(
        int(duration * SAMPLE_RATE_DEVICE),
        samplerate=SAMPLE_RATE_DEVICE,
        channels=1,
        dtype='float32',
        device=MIC_DEVICE
    )
    sd.wait()
    if SAMPLE_RATE_DEVICE != SAMPLE_RATE_WHISPER:
        audio_out = scipy.signal.resample_poly(
            audio.flatten(), SAMPLE_RATE_WHISPER, SAMPLE_RATE_DEVICE)
    else:
        audio_out = audio.flatten()
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        wav.write(f.name, SAMPLE_RATE_WHISPER,
                  (audio_out * 32767).astype(np.int16))
        result = _model.transcribe(f.name, fp16=False, language='en')
    text = result['text'].strip()
    print(f"[LISTEN] Heard: {text}")
    return text
