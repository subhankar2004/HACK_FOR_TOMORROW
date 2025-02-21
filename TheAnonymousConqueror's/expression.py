import cv2
import numpy as np
from tensorflow.keras.models import load_model
import pyttsx3  # For text-to-speech

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

# Load the pre-trained emotion detection model (you can use FER+ or similar)
model = load_model("facialemotionmodel.h5")  # Replace with your model's path
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Initialize the webcam
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Track the last spoken emotion to avoid repeated speech
last_spoken_emotion = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Preprocess the face for emotion recognition
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48))  # Resize to the input size of the model
        roi_gray = roi_gray / 255.0  # Normalize pixel values
        roi_gray = np.expand_dims(roi_gray, axis=0)  # Add batch dimension
        roi_gray = np.expand_dims(roi_gray, axis=-1)  # Add channel dimension
        
        # Predict the emotion
        predictions = model.predict(roi_gray)
        max_index = np.argmax(predictions[0])
        confidence = predictions[0][max_index]
        emotion = emotion_labels[max_index]
        
        # Display the emotion and confidence on the frame
        cv2.putText(frame, f"{emotion} ({confidence*100:.1f}%)", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        
        # Speak the emotion if it changes or confidence is high enough for Neutral
        if emotion == 'Neutral' and confidence < 0.6:  # Skip Neutral with low confidence
            continue
        
        if emotion != last_spoken_emotion:
            engine.say(f"{emotion}")
            engine.runAndWait()
            last_spoken_emotion = emotion
    
    # Display the output
    cv2.imshow('Emotion Detection', frame)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()