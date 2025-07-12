import paho.mqtt.client as mqtt
import json

# MQTT configuration
MQTT_BROKER = "192.168.0.100"  # IP address of the PC running the dashboard
MQTT_PORT = 1883

TOPIC_STATE = "safestart/state"         # Pi → PC (system state)
TOPIC_OVERRIDE = "safestart/override"   # PC → Pi (manual override)

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

override_command = None  # Will hold the last override command received

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code", rc)
    client.subscribe("safestart/override")

def on_message(client, userdata, msg):
    print("Ran")
    global override_command
    if msg.topic == "safestart/override":
        try:
            payload = json.loads(msg.payload.decode())
            override_command = payload.get("command")
            print("Override received:", override_command)
        except Exception as e:
            print("Invalid override message:", e)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()


# Function to publish sensor and system state to the PC
def send_state_to_dashboard(state, plan, motor_on, fan_on):
    payload = {
        "temperature": state.get("temperature"),
        "humidity": state.get("humidity"),
        "light": state.get("light"),
        "motion": "Yes" if state.get("motion") == 1 else "No",
        "emergency": "Emergency Stop" if state.get("emergency_active") else "Not Active",
        "fire": state.get("fire_detected"),
        "occupancy_zone1": state.get("occupancy_zone1"),
        "occupancy_zone2": state.get("occupancy_zone2"),
        "motor": "ON" if motor_on else "OFF",
        "fan": "ON" if fan_on else "OFF",
        "last_plan": plan
    }
    mqtt_client.publish("safestart/state", json.dumps(payload))

# Function to check if manual override was received from PC
def check_for_override():
    global override_command
    cmd = override_command
    #print(cmd)
    override_command = None  # Clear after reading
    return cmd
