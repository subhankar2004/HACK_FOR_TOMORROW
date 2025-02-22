import cv2
import base64
import google.generativeai as genai
import mtranslate
import pyttsx3
import time
import os
import re  # Import regex module for text cleaning

# Configure the API key
genai.configure(api_key="")

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 180)

def speak(audio):
    translated_audio = mtranslate.translate(audio, to_language="te-IN", from_language="te-IN")
    print(translated_audio)
    engine.say(translated_audio)
    engine.runAndWait()

# Function to remove unwanted characters (*, #, etc.)
def clean_text(text):
    cleaned_text = re.sub(r"[*#]", "", text)  # Remove * and # symbols
    return cleaned_text.strip()  # Remove extra spaces

# Function to capture an image from the phone camera
def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access phone camera.")
        return None

    print("Capturing photo...")
    
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        cap.release()
        return None

    cap.release()

    # Display the captured image in a window
    cv2.imshow("Captured Image", frame)
    cv2.waitKey(0)  # Wait until a key is pressed
    cv2.destroyAllWindows()

    # Save the image in the 'photos' folder
    photos_folder = "photos"
    if not os.path.exists(photos_folder):
        os.makedirs(photos_folder)

    image_path = os.path.join(photos_folder, f"photo_{int(time.time())}.jpg")
    cv2.imwrite(image_path, frame)
    print(f"Image saved at {image_path}")

    return frame

# Main function to process the captured image and query the API
def main():
    frame = capture_image()
    if frame is None:
        return

    # Encode the image in Base64
    _, buffer = cv2.imencode(".jpg", frame)
    image_data = base64.b64encode(buffer).decode('utf-8')

    # Prompt for the AI model
    prompt = "What is there in this picture?"

    # Initialize the Generative Model
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    # Generate content
    response = model.generate_content([
        {'mime_type': 'image/jpeg', 'data': image_data},
        prompt
    ])

    # Clean the response text
    clean_response = clean_text(response.text)

    # Print and speak the response
    print(clean_response)
    speak(clean_response)

if __name__ == "__main__":
    main()
