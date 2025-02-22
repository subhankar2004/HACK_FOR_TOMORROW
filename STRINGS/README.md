# DANCE-ZERO: AI-POWERED DANCE ACCURACY AND STEP CORRECTION APP

## Introduction

Dance-Zero is an AI-powered application designed to improve dance learning efficiency by analyzing body movements, detecting dance steps, and providing real-time corrections. The system utilizes advanced pose estimation techniques and machine learning algorithms to guide users towards accurate movements.

## Tech Stack

### Backend (Flask-based API)

- Flask - Lightweight web framework for API development
- OpenCV - Video processing and real-time body detection
- MediaPipe - Pose estimation and landmark extraction
- Matplotlib - Visualization of dance movements
- SciPy - Euclidean distance calculations for movement accuracy
- FastData - Performance optimization for real-time processing
- NumPy - Numerical computation and matrix operations

### Frontend (React-based UI)

- React.js (CRA) - Component-based UI architecture
- JavaScript - Frontend logic and API integration
- CSS - Styling and responsive design

## System Architecture

1. Admin Video Upload:
   - Admin uploads dance tutorial videos (Basic to Advanced).
   - Videos are processed and key movement landmarks are extracted.
2. User Pose Detection & Comparison:

   - User upload video; real-time video is processed using OpenCV.
   - MediaPipe extracts body landmarks (joints, angles, facial points).
   - Pose landmarks from the user’s video are compared with reference dance movements using Euclidean distance and angle betwwen different body parts (Eg. - elbow, shoulder, knee, wrist, hip-join, ankle).

3. Performance Evaluation:
   - Visual analytics using Matplotlib to compare user’s performance against the reference dance.
   - Generates insights on accuracy, posture deviations, and improvement areas.

## Key Features

- Pose Estimation: Real-time body tracking via MediaPipe/OpenCV.
- Step Correction: AI-based feedback with visual guidance.
- Accuracy Rating: Quantitative movement analysis using machine learning models.
- User-friendly UI: React.js frontend for an interactive experience.
- Scalability: Optimized with FastData for smooth real-time processing.

## Installation & Setup

### Backend Setup

```bash
mkdir backend
pip install flask opencv-python mediapipe matplotlib scipy fastdata numpy
python app.py  # Start Flask server
```

### Frontend Setup

```bash
npx create-react-app danceui
cd danceui
npm install
npm start  # Start React frontend
```

## USE GENERATIVE AI API

## Future Scope

- AI-driven movement analysis reports for professional training.
- Expansion to yoga, martial arts, and physiotherapy.
- Cloud-based analytics for personalized learning.

## Conclusion

Dance-Zero leverages AI and computer vision to democratize dance learning by providing real-time feedback and correction. This innovative approach enhances accessibility to high-quality dance training, revolutionizing self-paced learning experiences.
