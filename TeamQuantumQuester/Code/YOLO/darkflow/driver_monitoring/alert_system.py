from twilio.rest import Client

ACCOUNT_SID = "ACe06594b00f64e155206a5491eda7f5a1"
AUTH_TOKEN = "0bfab324136c9266ce270ad60df04991"
TWILIO_PHONE = "+15866493437"
EMERGENCY_PHONE = "+916376122867"

def send_alert(message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=EMERGENCY_PHONE
    )
    print("Alert sent!")
