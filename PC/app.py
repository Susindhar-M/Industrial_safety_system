from flask import Flask, render_template, request, jsonify
import threading
import paho.mqtt.client as mqtt
import json




MQTT_BROKER = "0.0.0.0"
MQTT_PORT = 1883

app = Flask(__name__)

# Shared state
state = {
    "temperature": None,
    "humidity": None,
    "light": None,
    "motion": False,
    "fire": False,
    "emergency": False,
    "occupancy_zone1": 0,
    "occupancy_zone2": 0,
    "motor": "OFF",
    "fan": "OFF",
    "last_plan": []
}

override_command = None  # 'on', 'off', or None

# MQTT client setup
MQTT_BROKER = "localhost"
MQTT_TOPIC_STATE = "safestart/state"
MQTT_TOPIC_OVERRIDE = "safestart/override"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("MQTT connected")
    client.subscribe(MQTT_TOPIC_STATE)

def on_message(client, userdata, msg):
    global state
    if msg.topic == MQTT_TOPIC_STATE:
        try:
            import json
            incoming = json.loads(msg.payload.decode())
            state.update(incoming)
        except Exception as e:
            print("Failed to update state:", e)

def mqtt_thread():
    #client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()

# Start MQTT in a separate thread
threading.Thread(target=mqtt_thread, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html", state=state)

@app.route("/override", methods=["POST"])
def override():
    global override_command
    cmd = request.json.get("command")
    if cmd in ["on", "off","auto"]:
        override_command = cmd
        client.publish("safestart/override", json.dumps({"command": cmd}))  # <-- Add this
    return '', 204

@app.route("/check_override")
def check_override():
    global override_command
    if override_command:
        cmd = override_command
        override_command = None
        return jsonify({"command": cmd})
    return jsonify({})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
