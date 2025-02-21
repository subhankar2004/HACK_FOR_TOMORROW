import cv2
import numpy as np
from ultralytics import YOLO 
import mediapipe as mp

video_path = r"C:\WoSAAP\Voilence Against Woman DATASET\WhatsApp Video 2025-02-17 at 05.25.36_81385523.mp4"

# Load YOLOv8 Model
model = YOLO("yolov8n.pt")

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
# Open the video file
cap = cv2.VideoCapture(video_path)   
assert cap.isOpened(), "Error: Could not open video file"

import requests
import datetime

API_URL = "http://127.0.0.1:8000/log-violence/"

# Open a log file in append mode
log_file = open("violence_log.txt", "a")

# Parameters for Shi-Tomasi Corner Detection
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

# Parameters for Lucas-Kanade Optical Flow
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Read the First Frame
ret, old_frame = cap.read()
if not ret:
    print("Error: Cannot read video frame")
    cap.release()
    exit()

old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
mask = np.zeros_like(old_frame)  # Mask for motion vectors

# Detect People Using YOLO
results = model(old_frame)
people_boxes = []

for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        if class_id == 0:  # Only process persons
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            people_boxes.append((x1, y1, x2, y2))

# Detect Shi-Tomasi Corners in Human Regions
p0 = []
for (x1, y1, x2, y2) in people_boxes:
    roi = old_gray[y1:y2, x1:x2]
    keypoints = cv2.goodFeaturesToTrack(roi, mask=None, **feature_params)
    if keypoints is not None:
        keypoints[:, 0, 0] += x1
        keypoints[:, 0, 1] += y1
        p0.extend(keypoints)

if len(p0) > 0:
    p0 = np.array(p0, dtype=np.float32)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect People Again for Tracking
    results = model(frame)
    people_boxes = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            if class_id == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                people_boxes.append((x1, y1, x2, y2))

    # Compute Optical Flow
    if p0 is not None and len(p0) > 0:
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        if p1 is not None:
            good_new = p1[st == 1]
            good_old = p0[st == 1]

            motion_energy = 0
            for (new, old) in zip(good_new, good_old):
                a, b = new.ravel()
                c, d = old.ravel()
                motion_vector = np.array([a - c, b - d])
                motion_energy += np.linalg.norm(motion_vector)

                mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
                frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 0, 255), -1)

    # Detect Pose and Analyze for Violent Actions
    violence_detected = False

    for (x1, y1, x2, y2) in people_boxes:
        person_roi = frame[y1:y2, x1:x2]
        person_rgb = cv2.cvtColor(person_roi, cv2.COLOR_BGR2RGB)

        # Run Pose Estimation
        results = pose.process(person_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Extract Key Joint Coordinates
            left_hand = np.array([landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * frame.shape[1],
                                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * frame.shape[0]])

            right_hand = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * frame.shape[1],
                                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * frame.shape[0]])

            left_elbow = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * frame.shape[1],
                                   landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * frame.shape[0]])

            right_elbow = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x * frame.shape[1],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y * frame.shape[0]])

            # Compute Speed (Magnitude of Movement)
            hand_speed = np.linalg.norm(left_hand - left_elbow) + np.linalg.norm(right_hand - right_elbow)

            if motion_energy > 800 and hand_speed > 50:  # Tune Threshold
                violence_detected = True
            if violence_detected:
                # Get current timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Log in the file
                log_file.write(f"{timestamp} - Violence Detected\n")
                log_file.flush()  # Ensure data is written immediately

                # Send data to the API
                log_data = {
                    "timestamp": timestamp,
                    "location": "CCTV-12, Main Street",  # Modify as needed
                    "details": "Violence Detected in video frame."
                }
                try:
                    response = requests.post(API_URL, json=log_data)
                    print(response.json())  # Print API response
                except Exception as e:
                    print(f"Error sending log to API: {e}")

                # Display the alert in the video output
                cv2.putText(frame, "Violence Detected!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (0, 0, 255), 3)  # Red color alert

                # Also print in the terminal
                print("⚠️  Violence Detected in the video frame!")
                
    # Display Result
    output = cv2.add(frame, mask)
    cv2.imshow("Output", output)  # "Output" is the window name

    # Wait for key press and check exit condition
    key = cv2.waitKey(1)  # Only call it once
    if key == ord('q') or key == 27:  # 27 is ESC key
        break
    
    # Update Previous Frame and Points
    old_gray = frame_gray.copy()

    # Detect New Keypoints for Next Frame
    p0 = []
    for (x1, y1, x2, y2) in people_boxes:
        roi = old_gray[y1:y2, x1:x2]
        keypoints = cv2.goodFeaturesToTrack(roi, mask=None, **feature_params)
        if keypoints is not None:
            keypoints[:, 0, 0] += x1
            keypoints[:, 0, 1] += y1
            p0.extend(keypoints)

    if len(p0) > 0:
        p0 = np.array(p0, dtype=np.float32)

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
            
# Close the log file at the end
log_file.close()

response = requests.get("http://127.0.0.1:8000/get-logs/")
print(response.json())
