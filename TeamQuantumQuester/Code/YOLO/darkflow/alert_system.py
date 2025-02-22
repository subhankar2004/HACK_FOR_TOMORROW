from twilio.rest import Client

# Twilio API Credentials
ACCOUNT_SID = "ACff8ece302b2928eb7da312ec9456649f"
AUTH_TOKEN = "5f7a8cf6ce638a7e8fbed7398be23d44"
TWILIO_PHONE = "+17373719357"
POLICE_PHONE = "+919040512369"

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
