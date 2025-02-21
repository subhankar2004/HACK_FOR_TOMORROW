import speech_recognition as sr
from twilio.rest import Client

# Twilio configuration
ACCOUNT_SID = "ACf4330a19b39789df0be5ab746ece8b80"
AUTH_TOKEN = "6201181a2d9c71f181635c9d2cdb282b"
TWILIO_PHONE_NUMBER = "+12313071633"
# POLICE_NUMBER = "+916300505459"
# HOSPITAL_NUMBER = "+916300505459"
EMERGENCY_CONTACT = "+916300505459"


client = Client(ACCOUNT_SID, AUTH_TOKEN)

def make_call(to_number, message):
    """Makes a call and speaks a message."""
    try:
        call = client.calls.create(
            twiml=f"<Response><Say>{message}</Say></Response>",
            to=to_number,
            from_=TWILIO_PHONE_NUMBER
        )
        print(f"Call initiated to {to_number}. SID: {call.sid}")
    except Exception as e:
        print(f"Error making call: {e}")

def listen_and_process():
    # """Listens to the microphone and processes keywords."""
    # recognizer = sr.Recognizer()
    # microphone = sr.Microphone()

    # print("Listening for 'help' or 'emergency'...")
    # with microphone as source:
    #     recognizer.adjust_for_ambient_noise(source)
    #     try:
    #         audio = recognizer.listen(source, timeout=10)
    #         command = recognizer.recognize_google(audio).lower()
    #         print(f"Heard: {command}")

    #         if "help" in command:
    #             print("Calling police station and emergency contact...")
                # make_call(POLICE_NUMBER, "This is an automated call. Help is needed at the reported location.")
                make_call(EMERGENCY_CONTACT, "This is an automated call. Help is needed at the reported location.")

        #     elif "emergency" in command:
        #         print("Calling police station, hospital, and emergency contact...")
        #         make_call(POLICE_NUMBER, "This is an automated call. Emergency reported. Immediate assistance required.")
        #         make_call(HOSPITAL_NUMBER, "This is an automated call. Medical emergency reported. Immediate assistance required.")
        #         make_call(EMERGENCY_CONTACT, "This is an automated call. Emergency reported. Immediate assistance required.")

        #     else:
        #         print("No relevant keywords detected.")

        # except sr.UnknownValueError:
        #     print("Could not understand the audio.")
        # except sr.RequestError as e:
        #     print(f"Could not request results; {e}")
        # except Exception as e:
        #     print(f"Error: {e}")

if __name__ == "__main__":
    # while True:
        listen_and_process()