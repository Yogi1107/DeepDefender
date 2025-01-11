# Webcam Face Detection Project

This project uses OpenCV and Flask to create a real-time webcam face detection application. The application detects faces in the webcam feed, saves the images of detected faces, and displays the webcam feed on a webpage. It is built using Python, Flask for the web framework, and OpenCV for face detection.

## Features

- **Real-time Face Detection**: Detect faces from the webcam feed.
- **Image Saving**: Detected faces are saved in a dedicated folder with filenames based on face position and timestamp.
- **Web Interface**: The webcam feed is streamed to a web interface using Flask.
- **Dynamic Folder Creation**: A folder to save images is created automatically when the application runs.

## Prerequisites

Before you begin, ensure that you have the following installed:

- **Python 3.x**
- **pip** (Python package installer)

### Required Libraries

1. Flask
2. OpenCV
3. Werkzeug

You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt
