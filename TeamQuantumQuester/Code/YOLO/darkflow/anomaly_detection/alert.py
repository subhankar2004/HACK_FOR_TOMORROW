from twilio.rest import Client

# Twilio API Credentials
ACCOUNT_SID = "a1"
AUTH_TOKEN = "b"
TWILIO_PHONE = ""
POLICE_PHONE = ""

def send_alert(anomalies_detected):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    alert_message = "⚠ Vehicle Anomaly Detected: \n"
    for vehicle, anomaly in anomalies_detected:
        alert_message += f"{vehicle}: {anomaly}\n"

    message = client.messages.create(
        body=alert_message,
        from_=TWILIO_PHONE,
        to=POLICE_PHONE
    )

    print(f"🚨 Alert sent to police: {alert_message}")
