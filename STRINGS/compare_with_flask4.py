from flask import Flask, request, render_template, jsonify
import cv2
import numpy as np
import mediapipe as mp
import os
import time
from scipy.spatial.distance import cosine
from fastdtw import fastdtw  # Changed import
from scipy.spatial.distance import euclidean  # Required for fastdtw

app = Flask(__name__)

# Initialize MediaPipe Pose with higher confidence thresholds
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,  # Use the most accurate model
    smooth_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Define important keypoints for pose comparison
IMPORTANT_KEYPOINTS = [
    11, 12,  # shoulders
    13, 14,  # elbows
    15, 16,  # wrists
    23, 24,  # hips
    25, 26,  # knees
    27, 28   # ankles
]

# Function to extract pose keypoints with normalized coordinates
def extract_keypoints(frame):
    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if not results.pose_landmarks:
        return None
    
    # Get all landmarks
    keypoints = np.array([[lm.x, lm.y, lm.z, lm.visibility] 
                          for lm in results.pose_landmarks.landmark])
    
    # Normalize positions relative to hip center
    hip_center = (keypoints[23][:3] + keypoints[24][:3]) / 2
    normalized_keypoints = keypoints.copy()
    
    for i in range(len(normalized_keypoints)):
        normalized_keypoints[i][:3] = normalized_keypoints[i][:3] - hip_center
    
    return normalized_keypoints

# Function to calculate joint angles
def calculate_angles(keypoints):
    if keypoints is None:
        return None
    
    angles = []
    
    # Right arm angle (shoulder-elbow-wrist)
    v1 = keypoints[11][:3] - keypoints[13][:3]
    v2 = keypoints[15][:3] - keypoints[13][:3]
    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    angles.append(angle)
    
    # Left arm angle (shoulder-elbow-wrist)
    v1 = keypoints[12][:3] - keypoints[14][:3]
    v2 = keypoints[16][:3] - keypoints[14][:3]
    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    angles.append(angle)
    
    # Right leg angle (hip-knee-ankle)
    v1 = keypoints[23][:3] - keypoints[25][:3]
    v2 = keypoints[27][:3] - keypoints[25][:3]
    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    angles.append(angle)
    
    # Left leg angle (hip-knee-ankle)
    v1 = keypoints[24][:3] - keypoints[26][:3]
    v2 = keypoints[28][:3] - keypoints[26][:3]
    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    angles.append(angle)
    
    return np.array(angles)

# Function to calculate multi-metric similarity
def calculate_similarity(kp1, kp2):
    if kp1 is None or kp2 is None:
        return 0
    
    # 1. Calculate position similarity for important keypoints
    position_similarity = 0
    visible_count = 0
    
    for idx in IMPORTANT_KEYPOINTS:
        # Only consider keypoints that are visible in both frames
        if kp1[idx][3] > 0.5 and kp2[idx][3] > 0.5:
            # Euclidean distance between keypoints
            dist = np.linalg.norm(kp1[idx][:3] - kp2[idx][:3])
            position_similarity += np.exp(-dist * 5)  # Higher weight for position
            visible_count += 1
    
    if visible_count == 0:
        return 0
    
    position_similarity /= visible_count
    
    # 2. Calculate angle similarity
    angles1 = calculate_angles(kp1)
    angles2 = calculate_angles(kp2)
    
    if angles1 is None or angles2 is None:
        angle_similarity = 0
    else:
        # Cosine similarity between angle vectors
        angle_similarity = 1 - cosine(angles1, angles2)
        if np.isnan(angle_similarity):
            angle_similarity = 0
    
    # 3. Calculate pose vector similarity
    # Flatten important keypoints to vectors
    vec1 = np.concatenate([kp1[idx][:3] for idx in IMPORTANT_KEYPOINTS])
    vec2 = np.concatenate([kp2[idx][:3] for idx in IMPORTANT_KEYPOINTS])
    
    # Cosine similarity between pose vectors
    vector_similarity = 1 - cosine(vec1, vec2) if not np.isnan(vec1).any() and not np.isnan(vec2).any() else 0
    if np.isnan(vector_similarity):
        vector_similarity = 0
    
    # Weighted combination of similarities
    final_similarity = (0.5 * position_similarity + 
                        0.3 * angle_similarity + 
                        0.2 * vector_similarity)
    
    return final_similarity

@app.route('/')
def index():
    return render_template('index4.html')

@app.route('/compare', methods=['POST'])
def compare_videos():
    if 'video1' not in request.files or 'video2' not in request.files:
        return jsonify({"error": "Both video files are required"}), 400

    video1 = request.files['video1']
    video2 = request.files['video2']

    # Ensure uploads directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # Save videos temporarily
    video1_path = os.path.join('uploads', video1.filename)
    video2_path = os.path.join('uploads', video2.filename)
    
    try:
        video1.save(video1_path)
        video2.save(video2_path)
    except Exception as e:
        return jsonify({"error": f"File saving error: {str(e)}"}), 500

    # Load videos
    try:
        cap1 = cv2.VideoCapture(video1_path)
        cap2 = cv2.VideoCapture(video2_path)

        if not cap1.isOpened() or not cap2.isOpened():
            return jsonify({"error": "Could not open video files"}), 400

        # Get video information
        fps1 = cap1.get(cv2.CAP_PROP_FPS)
        fps2 = cap2.get(cv2.CAP_PROP_FPS)
        
        # Extract pose sequences
        seq1 = []
        seq2 = []
        
        # Extract reference video poses
        while True:
            ret, frame = cap1.read()
            if not ret:
                break
            
            frame = cv2.resize(frame, (640, 480))
            keypoints = extract_keypoints(frame)
            if keypoints is not None:
                seq1.append(keypoints)
        
        # Extract user video poses
        while True:
            ret, frame = cap2.read()
            if not ret:
                break
            
            frame = cv2.resize(frame, (640, 480))
            keypoints = extract_keypoints(frame)
            if keypoints is not None:
                seq2.append(keypoints)
        
        # Check if we have enough frames
        if len(seq1) < 5 or len(seq2) < 5:
            return jsonify({"error": "Videos too short or no poses detected"}), 400
        
        # Sample frames to handle different video lengths
        if len(seq1) > len(seq2):
            # Downsample seq1
            indices = np.linspace(0, len(seq1)-1, len(seq2)).astype(int)
            seq1 = [seq1[i] for i in indices]
        elif len(seq2) > len(seq1):
            # Downsample seq2
            indices = np.linspace(0, len(seq2)-1, len(seq1)).astype(int)
            seq2 = [seq2[i] for i in indices]
        
        # Temporal comparison frame by frame
        frame_similarities = []
        detailed_feedback = []
        
        for i in range(len(seq1)):
            # Get frame similarity
            similarity = calculate_similarity(seq1[i], seq2[i])
            frame_similarities.append(similarity)
            
            # Add detailed feedback for significant deviations
            if similarity < 0.7:
                angles1 = calculate_angles(seq1[i])
                angles2 = calculate_angles(seq2[i])
                
                if angles1 is not None and angles2 is not None:
                    # Check which body part has the largest deviation
                    angle_diffs = np.abs(angles1 - angles2)
                    max_diff_idx = np.argmax(angle_diffs)
                    
                    if max_diff_idx == 0:
                        detailed_feedback.append(f"Frame {i}: Check right arm position")
                    elif max_diff_idx == 1:
                        detailed_feedback.append(f"Frame {i}: Check left arm position")
                    elif max_diff_idx == 2:
                        detailed_feedback.append(f"Frame {i}: Check right leg position")
                    elif max_diff_idx == 3:
                        detailed_feedback.append(f"Frame {i}: Check left leg position")
        
        # Overall accuracy is the average similarity
        overall_accuracy = np.mean(frame_similarities) * 100
        
        # Find the timestamps with lowest similarity
        if len(frame_similarities) > 0:
            worst_frames = np.argsort(frame_similarities)[:3]
            timestamps = [f"{int(i / fps1 // 60)}:{int(i / fps1 % 60)}" for i in worst_frames]
            improvement_areas = [f"Check posture at {timestamp}" for timestamp in timestamps]
        else:
            improvement_areas = ["Could not identify specific areas for improvement"]
        
        # Prepare detailed feedback
        detailed_feedback = detailed_feedback[:5]  # Limit to 5 most significant issues
        
        result = {
            "accuracy": f"{overall_accuracy:.2f}%",
            "improvement_areas": improvement_areas,
            "detailed_feedback": detailed_feedback
        }

    except Exception as e:
        result = {"error": f"Processing error: {str(e)}"}
    
    finally:
        # Release videos if they were opened
        if 'cap1' in locals() and cap1.isOpened():
            cap1.release()
        if 'cap2' in locals() and cap2.isOpened():
            cap2.release()

        # Remove temporary files if they exist
        try:
            if os.path.exists(video1_path):
                os.remove(video1_path)
            if os.path.exists(video2_path):
                os.remove(video2_path)
        except Exception as e:
            print(f"Error removing temporary files: {str(e)}")

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)