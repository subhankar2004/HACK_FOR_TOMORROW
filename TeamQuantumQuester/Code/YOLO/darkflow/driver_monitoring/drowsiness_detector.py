# drowsiness_detector.py
import cv2
import face_recognition
import numpy as np
import time
from alert_system import send_alert

def eye_aspect_ratio(eye):
    """
    Compute the eye aspect ratio (EAR) using the Euclidean distances between the eye landmarks.
    The formula uses two vertical distances and one horizontal distance.
    """
    # Convert points (tuples) to numpy arrays for distance calculations
    eye = np.array(eye)
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def detect_drowsiness():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    drowsy_frames = 0
    EAR_THRESHOLD = 0.25  # Eye Aspect Ratio threshold below which the eye is considered closed
    CONSEC_FRAMES = 15    # Number of consecutive frames of closed eyes to trigger alert

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert from BGR (OpenCV default) to RGB (face_recognition uses RGB)
        rgb_frame = frame[:, :, ::-1]

        # Locate faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_landmarks_list = face_recognition.face_landmarks(rgb_frame, face_locations)

        for face_landmarks in face_landmarks_list:
            # Get eye landmarks from the dictionary
            left_eye = face_landmarks.get('left_eye')
            right_eye = face_landmarks.get('right_eye')
            if left_eye and right_eye:
                left_ear = eye_aspect_ratio(left_eye)
                right_ear = eye_aspect_ratio(right_eye)
                ear = (left_ear + right_ear) / 2.0

                # Draw eye landmarks (optional)
                for point in left_eye + right_eye:
                    cv2.circle(frame, point, 2, (0, 255, 0), -1)

                cv2.putText(frame, f"EAR: {ear:.2f}", (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # Check if the average EAR is below the threshold
                if ear < EAR_THRESHOLD:
                    drowsy_frames += 1
                else:
                    drowsy_frames = 0

                # If eyes remain closed for a sufficient number of consecutive frames, trigger alert
                if drowsy_frames >= CONSEC_FRAMES:
                    cv2.putText(frame, "DROWSINESS DETECTED!", (30, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    send_alert("Driver drowsiness detected!")
                    drowsy_frames = 0  # Reset the counter after alert

        cv2.imshow("Drowsiness Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_drowsiness()
