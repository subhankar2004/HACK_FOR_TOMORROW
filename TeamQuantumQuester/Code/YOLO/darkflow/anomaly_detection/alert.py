from twilio.rest import Client

# Twilio API Credentials
ACCOUNT_SID = "ACe06594b00f64e155206a5491eda7f5a1"
AUTH_TOKEN = "0bfab324136c9266ce270ad60df04991"
TWILIO_PHONE = "+15866493437"
POLICE_PHONE = "+916376122867"

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
