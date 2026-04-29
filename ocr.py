import cv2
import os
from datetime import datetime
from config import CAMERA_INDEX, CAPTURES_DIR

def capture_image() -> tuple:
    """Capture image from camera and save it."""
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        return None, None

    # Allow camera to adjust exposure
    for _ in range(10):
        ret, frame = cap.read()
    cap.release()

    if not ret:
        return None, None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_path = os.path.join(CAPTURES_DIR, f"capture_{timestamp}.jpg")
    cv2.imwrite(img_path, frame)
    print(f"[CAMERA]: Saved to {img_path}")
    return frame, img_path
