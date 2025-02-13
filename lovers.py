import cv2
import random
import time
import numpy as np

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to detect faces in an image
def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

# Function to draw the compatibility gauge with Valentine's theme
def draw_gauge(image, compatibility):
    gauge_width = 400
    gauge_height = 30
    gauge_x = (image.shape[1] - gauge_width) // 2
    gauge_y = image.shape[0] - 100  # Move gauge higher for better visibility

    # Draw the gauge background (white border)
    cv2.rectangle(image, (gauge_x, gauge_y), (gauge_x + gauge_width, gauge_y + gauge_height), (255, 255, 255), 2)

    # Draw the filled gauge based on compatibility (pink color for Valentine's theme)
    fill_width = int(gauge_width * (compatibility / 100))
    cv2.rectangle(image, (gauge_x, gauge_y), (gauge_x + fill_width, gauge_y + gauge_height), (180, 105, 255), -1)  # Pink color

    # Add text for the compatibility percentage (with heart symbol)
    cv2.putText(image, f'{compatibility}% <3', (gauge_x + gauge_width + 10, gauge_y + gauge_height // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (180, 105, 255), 2)  # Pink color

# Function to add Valentine-themed text
def draw_valentine_text(image, message):
    text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x = (image.shape[1] - text_size[0]) // 2
    text_y = (image.shape[0] - text_size[1]) // 2

    # Add a shadow effect for the text
    cv2.putText(image, message, (text_x + 2, text_y + 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)  # Black shadow
    cv2.putText(image, message, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # Red text

# Capture video from the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Variables to track steady faces
steady_start_time = None
compatibility = None
message = None

def reset_compatibility():
    global compatibility, steady_start_time, message
    compatibility = None
    steady_start_time = None
    message = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = detect_faces(frame)

    if len(faces) == 2:  # Exactly two faces detected
        if steady_start_time is None:
            steady_start_time = time.time()  # Start the timer
        else:
            elapsed_time = time.time() - steady_start_time
            cv2.putText(frame, f'Compatibility in {5 - int(elapsed_time)} sec... <3', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (180, 105, 255), 2)  # Pink text
            if elapsed_time >= 5 and compatibility is None:  # Faces steady for 5 seconds
                compatibility = random.randint(30, 100)
                if 30 <= compatibility <= 40:
                    message = 'Better luck in the next life... </3'
                elif 50 <= compatibility <= 60:
                    message = 'Being friends is good... I guess <3'
                elif 65 <= compatibility <= 70:
                    message = 'Something is blooming mwehehe <3'
                elif 75 <= compatibility <= 80:
                    message = 'I wish I could feel both your love. <3'
                elif 85 <= compatibility <= 90:
                    message = 'Hmm... Love does exist between you two. <3'
                elif 95 <= compatibility <= 100:
                    message = 'Do I hear wedding bells? <3'
    else:
        if steady_start_time is not None:
            steady_start_time = None  # Reset timer if not exactly two faces

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Draw the gauge and message if compatibility is set
    if compatibility is not None:
        draw_gauge(frame, compatibility)
        if message:
            draw_valentine_text(frame, message)
    else:
        cv2.putText(frame, 'Detecting friends? or... lovers? <3', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (180, 105, 255), 2)  # Pink text

    cv2.imshow('Face Detection and Compatibility', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):  # Spacebar pressed to reset compatibility
        reset_compatibility()

cap.release()
cv2.destroyAllWindows()