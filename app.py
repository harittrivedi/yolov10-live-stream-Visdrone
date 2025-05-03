from flask import Flask, Response
import cv2
from ultralytics import YOLO

# Load your YOLOv10 model
model = YOLO('best.pt')

# Open webcam
cap = cv2.VideoCapture(0)  # 0 = default camera
cap.set(3, 640)
cap.set(4, 480)

app = Flask(__name__)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Inference
            results = model.predict(frame, imgsz=640, conf=0.5)
            annotated_frame = results[0].plot()

            # Encode frame
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()

            # Stream the frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "YOLOv10 Live Stream - Go to /video"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
