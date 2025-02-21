import cv2
import time
from score_system import update_score


# Load OpenCV face/eye detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)  # Open webcam

DROWSY_THRESHOLD = 3  # Number of seconds to be considered drowsy
start_time = None
is_drowsy = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        if start_time is None:
            start_time = time.time()
        elif time.time() - start_time >= DROWSY_THRESHOLD:
            if not is_drowsy:
                print("🚨 Drowsiness detected! Deducting points...")
                update_score(10)  # Deduct points
                is_drowsy = True
    else:
        start_time = None
        is_drowsy = False

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Drowsiness Monitor', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
