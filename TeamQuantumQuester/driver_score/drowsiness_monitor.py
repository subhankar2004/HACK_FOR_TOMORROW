import cv2
import time
from score_system import update_score

# Load OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)  # Open webcam

DROWSY_THRESHOLD = 3  # Seconds without a detected face to consider as drowsy
start_time = None
is_drowsy = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        if start_time is None:
            start_time = time.time()
        elapsed = time.time() - start_time
        cv2.putText(frame, f"No face detected: {elapsed:.1f}s", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        if elapsed >= DROWSY_THRESHOLD and not is_drowsy:
            print("🚨 Drowsiness detected! Deducting points...")
            update_score(10)  # Deduct points
            is_drowsy = True
            cv2.putText(frame, "Drowsiness Detected!", (10, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    else:
        start_time = None
        is_drowsy = False
        cv2.putText(frame, "Face Detected", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Drowsiness Monitor', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
