import cv2
import numpy as np
from ultralytics import YOLO
import mediapipe as mp
import threading
from queue import Queue
import supervision as sv

# Load Models
model = YOLO("yolov8n.pt")  

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# video_path = r"C:\\WoSAAP DATASET\\Voilence Against Woman DATASET\\WhatsApp Video 2025-02-16 at 20.29.05_0087f775.mp4"
# cap = cv2.VideoCapture(video_path)   
# assert cap.isOpened(), "Error: Could not open video file"


# Initialize Video Capture
cap = cv2.VideoCapture(0)  # Webcam (0) or path to video file

if not cap.isOpened():
    print("Error: Could not open video capture")
    exit()

# Optical Flow Parameters
# Shi-tomasi Prameters / Corner Detection
feature_params = dict(maxCorners=500, qualityLevel=0.3, minDistance=5, blockSize=4)

# Optical flow Parameters / Lucas Kanade Algorithm
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Initialize supervision annotators
box_annotator = sv.BoxCornerAnnotator(thickness=1)
rich_label_annotator = sv.RichLabelAnnotator(
    font_path="Roboto-VariableFont_wdth,wght.ttf",  # Replace with your font file
    text_position=sv.Position.CENTER
)

# Open a log file
log_file = open("violence_log.txt", "a")

# Create Windows
cv2.namedWindow("Original Video")
cv2.namedWindow("Person Detection")
cv2.namedWindow("Violence Detection")

class OpticalFlowProcessor:
    def __init__(self, lk_params, feature_params):
        self.lk_params = lk_params
        self.feature_params = feature_params
        self.mask = None

    def compute_optical_flow(self, frame_gray, p0, original_frame):
        if self.mask is None:
            self.mask = np.zeros_like(original_frame)
        frame = original_frame.copy()
        motion_energy = 0
        if p0 is not None and len(p0) > 0:
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **self.lk_params)
            if p1 is not None:
                good_new = p1[st == 1]
                good_old = p0[st == 1]

                for (new, old) in zip(good_new, good_old):
                    a, b = new.ravel()
                    c, d = old.ravel()
                    motion_vector = np.array([a - c, b - d])
                    motion_energy += np.linalg.norm(motion_vector)

                    cv2.line(self.mask, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
                    cv2.circle(frame, (int(a), int(b)), 5, (0, 0, 255), -1)

        return motion_energy, self.mask, frame

    def process(self, frame_gray, p0, original_frame):
        motion_energy, self.mask, frame = self.compute_optical_flow(frame_gray, p0, original_frame)
        return motion_energy, self.mask, frame

optical_flow_processor = OpticalFlowProcessor(lk_params, feature_params)

frame_count = 0
old_gray = None
p0 = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    if frame_count % 3 != 0:
        continue
    
    # Original Video Window (Show the original frame)
    cv2.imshow("Original Video", frame)

    if frame_count == 1:
        old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        optical_flow_processor.mask = np.zeros_like(frame)

        results = model(frame)
        people_boxes = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                if class_id == 0:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    people_boxes.append((x1, y1, x2, y2))

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

    # Person Detection
    results = model(frame, stream=True, conf=0.4)
    detections_list = []

    for r in results:
        boxes = r.boxes
        xyxy = boxes.xyxy.cpu().numpy().astype(int)
        conf = boxes.conf.cpu().numpy()
        class_ids = boxes.cls.cpu().numpy().astype(int)

        detections = sv.Detections(xyxy=xyxy, confidence=conf, class_id=class_ids)
        detections_list.append(detections)

    annotated_frame = frame.copy()

    for detections in detections_list:
        labels = [
            f"{model.names[class_id]} {confidence:.2f}"
            for class_id, confidence
            in zip(detections.class_id, detections.confidence)
        ]

        annotated_frame = box_annotator.annotate(scene=annotated_frame, detections=detections)
        annotated_frame = rich_label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)

    people_boxes = detections.xyxy.tolist() if detections else []

    # Violence Detection
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    motion_energy, mask, frame = optical_flow_processor.process(frame_gray, p0, frame.copy())

    q = Queue()

    def worker(frame_gray, p0, frame_copy):
        motion_energy, mask, frame_output = optical_flow_processor.compute_optical_flow(frame_gray, p0, frame_copy)
        q.put((motion_energy, mask, frame_output))
        
    frame_copy = frame.copy()

    optical_flow_thread = threading.Thread(target=worker, args=(frame_gray, p0, frame_copy))
    optical_flow_thread.start()
    optical_flow_thread.join()

    motion_energy, mask, frame = q.get()

    violence_detected = False

    if people_boxes:
        for (x1, y1, x2, y2) in people_boxes:
            person_roi = frame[y1:y2, x1:x2]
            person_rgb = cv2.cvtColor(person_roi, cv2.COLOR_BGR2RGB)

            results = pose.process(person_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                left_hand = np.array([landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * frame.shape[1],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * frame.shape[0]])
                right_hand = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * frame.shape[1],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * frame.shape[0]])

                left_elbow = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * frame.shape[1],
                                       landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * frame.shape[0]])
                right_elbow = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x * frame.shape[1],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y * frame.shape[0]])

                hand_speed = np.linalg.norm(left_hand - left_elbow) + np.linalg.norm(right_hand - right_elbow)

                if motion_energy > 500 and hand_speed > 40:
                  violence_detected = True
                  print("⚠️  Violence Detected!")
                  log_file.write(f"Frame {frame_count}: Violence detected (Motion Energy: {motion_energy}, Hand Speed: {hand_speed})\n")
                  # Display the alert in the video output
                  cv2.putText(frame, "Violence Detected!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                              1, (0, 0, 255), 3)  # Red color alert
                  
    if frame is None:
        print("Warning: frame is None")
        continue


    old_gray = frame_gray.copy()

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
        
        
    output = cv2.add(frame, mask)  # Combine frame and mask

    # Violence Detection Window (Show the combined output)
    cv2.imshow("Violence Detection", output)  

    # Person Detection Window (Show the annotated frame)
    cv2.imshow("Person Detection", annotated_frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
            
# Close the log file at the end
log_file.close()