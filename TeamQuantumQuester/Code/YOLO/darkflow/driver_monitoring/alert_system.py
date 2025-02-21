from twilio.rest import Client

ACCOUNT_SID = "ACe06594b00f64e155206a5491eda7f5a1"
AUTH_TOKEN = "10947f174167a25addeb2c622dc1a8eb"
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
