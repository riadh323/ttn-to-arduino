from flask import Flask, request
import requests

app = Flask(__name__)

# TODO: Hier deine echten Daten einsetzen!
IOTC_API_TOKEN = "bwWzODc2fIv7oIjo2MJ0zrH2Cuc8BN3SzB8mtykrXOxSndbkharPSgrLODS77uSZS"
THING_ID = "94d04d01-fd23-42f5-8010-f690b7932a5f"
PROP_TEMP = "5588027f-e45f-476d-97cf-9c9b07cd25d8"
PROP_HUM = "1284aa1c-367a-4153-9542-887c87c76d67"
PROP_PRESS = "8e0a33ea-bc4d-4d5e-ab6b-dfef5c5d50d5"

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
