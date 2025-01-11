import cv2
import os
from flask import Flask, render_template, Response

# Initialize Flask app
app = Flask(__name__)

# Create a folder to save images if it doesn't exist
output_folder = "detected_faces"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize webcam capture
video_capture = cv2.VideoCapture(0)
video_streaming = True  # Flag to control video streaming

def gen():
    global video_streaming
    while video_streaming:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Load the pre-trained Haar Cascade classifier for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Loop through each detected face
        for (x, y, w, h) in faces:
            # Draw a rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Crop the face from the frame
            face_roi = frame[y:y + h, x:x + w]
            
            # Save the cropped face as an image
            face_filename = f"detected_face_{x}_{y}.jpg"
            face_filepath = os.path.join(output_folder, face_filename)
            cv2.imwrite(face_filepath, face_roi)

        # Convert frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            break

        # Yield the frame as a response for the video stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_feed', methods=['POST'])
def stop_feed():
    global video_streaming
    video_streaming = False  # Stop the video feed
    video_capture.release()  # Release the webcam
    return 'Webcam feed stopped'

if __name__ == '__main__':
    try:
        app.run(debug=True, threaded=True)
    except KeyboardInterrupt:
        # Release the webcam and close OpenCV windows gracefully
        video_capture.release()
        cv2.destroyAllWindows()
