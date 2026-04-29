import cv2
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

frame_data = None
lock = threading.Lock()

HTML = b"""<!DOCTYPE html>
<html>
<head>
<title>Camera Preview</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background: #111;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: sans-serif;
}
img {
    width: 90vw;
    max-width: 900px;
    border-radius: 12px;
}
p { color: #555; margin-top: 14px; font-size: 13px; }
</style>
</head>
<body>
<img id="cam" src="/frame">
<p>LIVE CAMERA FEED - Jetson Orin Nano</p>
<script>
var img = document.getElementById("cam");
function refresh() { img.src = "/frame?" + Date.now(); }
img.onload = function() { setTimeout(refresh, 80); };
img.onerror = function() { setTimeout(refresh, 500); };
</script>
</body>
</html>"""

def capture_loop():
    global frame_data
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            _, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            with lock:
                frame_data = jpeg.tobytes()
        time.sleep(0.05)

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML)
        elif self.path.startswith('/frame'):
            with lock:
                data = frame_data
            if data:
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(data)

threading.Thread(target=capture_loop, daemon=True).start()
print("Camera preview at http://10.169.54.243:8080")
print("Ctrl+C to stop")
HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
