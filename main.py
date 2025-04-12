from flask import Flask, request
import requests

app = Flask(__name__)

# TODO: Hier deine echten Daten einsetzen!
IOTC_API_TOKEN = "DEIN_ARDUINO_API_KEY"
THING_ID = "DEINE_THING_ID"
PROP_TEMP = "PROPERTY_ID_TEMPERATUR"
PROP_HUM = "PROPERTY_ID_HUMIDITY"
PROP_PRESS = "PROPERTY_ID_PRESSURE"

def send_to_arduino(property_id, value):
    url = f"https://api2.arduino.cc/iot/v2/things/{THING_ID}/properties/{property_id}/publish"
    headers = {
        "Authorization": f"Bearer {IOTC_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = { "value": value }
    response = requests.put(url, headers=headers, json=payload)
    print(f"Arduino API response: {response.status_code}, {response.text}")

@app.route("/ttn-data", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        payload = data["uplink_message"]["decoded_payload"]
        send_to_arduino(PROP_TEMP, payload.get("temperature"))
        send_to_arduino(PROP_HUM, payload.get("humidity"))
        send_to_arduino(PROP_PRESS, payload.get("pressure"))
    except Exception as e:
        print("Fehler:", e)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
