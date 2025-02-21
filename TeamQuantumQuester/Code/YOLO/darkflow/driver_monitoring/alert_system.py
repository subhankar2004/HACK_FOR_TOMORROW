from twilio.rest import Client

ACCOUNT_SID = "1"
AUTH_TOKEN = ""
TWILIO_PHONE = ""
EMERGENCY_PHONE = ""

def send_alert(message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=EMERGENCY_PHONE
    )
    print("Alert sent!")
