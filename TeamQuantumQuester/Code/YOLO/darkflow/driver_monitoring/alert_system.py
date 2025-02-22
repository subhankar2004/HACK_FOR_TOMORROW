from twilio.rest import Client

ACCOUNT_SID = "AC7666da9162ccae7b6eb1d2a814d8c919"
AUTH_TOKEN = "b1561e3893aef2ad9eb2eb310b11ea5b"
TWILIO_PHONE = "+16182059804"
EMERGENCY_PHONE = "+919040512369"

def send_alert(message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=EMERGENCY_PHONE
    )
    print("Alert sent!")
