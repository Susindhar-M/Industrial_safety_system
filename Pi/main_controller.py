######################################################################################################
# Authors : Susindhar Manivasagan, Raksha Nagendra, Mansi Sharad Dongare
######################################################################################################
# Do not modify
# main.py

####### RUN THIS CODE ON TERMINAL ##########


import time
from actuators.relay import Relay
from actuators.servo import ServoController
from actuators.lcd_display import LCD
from actuators.buzzer_led import BuzzerLED
from sensors.sensor_reader import SensorReader
from rfid.rfid_reader import RFIDManager
from utils.occupancy_manager import OccupancyManager
from planning.problem_generator import generate_problem_file
from planning.planner_interface import run_planner
from dashboard_comm import send_state_to_dashboard, check_for_override  # Uses MQTT

emergency_active = False
override_mode = None  # "on", "off", or None

# Initialize components
relay = Relay()
servo = ServoController()
lcd = LCD()
buzzer_led = BuzzerLED()
sensors = SensorReader()
rfid = RFIDManager()
occupancy = OccupancyManager()

try:
    while True:
        # 1. Read sensors
        sensor_data = sensors.get_state()
        temp = sensor_data["temperature"]
        hum = sensor_data["humidity"]
        light = sensor_data["light"]
        motion = sensor_data["motion"]

        if sensor_data["button_pressed"]:
            emergency_active = not emergency_active
            print(f"Emergency state toggled: {emergency_active}")

        # 2. RFID detection
        tag_data = rfid.read_tags()
        if tag_data:
            tag_id = tag_data["tag"]
            zone = tag_data["zone"]
            tag_type = rfid.get_tag_type(tag_id)

            if tag_type in ["M", "O"]:
                access_granted = rfid.update_entry(tag_id, zone)
                if access_granted:
                    buzzer_led.access_granted(zone)
                    servo.open(zone)
                    time.sleep(3)
                    servo.close(zone)
                else:
                    buzzer_led.access_denied()
            else:
                buzzer_led.access_denied()

        # 3. Prepare AI planning state
        occ_state = rfid.get_state()
        state = {
            "temperature": temp,
            "humidity": hum,
            "light": light,
            "motion": motion,
            "emergency_active": emergency_active,
            "occupancy_zone1": occ_state["count1"],
            "occupancy_zone2": occ_state["count2"],
            "temperature_high": temp is not None and temp > 30,
            "humidity_high": hum is not None and hum > 70,
            "fire_detected": temp and temp > 40 and light and light > 600,
            "motion_detected": motion == 1,
            "overcapacity_zone1": occ_state["count1"] > 0,
            "overcapacity_zone2": occ_state["count2"] > 3
        }

        # 4. Generate PDDL problem and 5. Run planner
        generate_problem_file(state)
        plan = run_planner()

        # 6. Check MQTT override
        command = check_for_override()
        if command in ["on", "off", "auto"]:
            override_mode = None if command == "auto" else command

        # 7. Execute actions
        motor_on = False
        fan_on = False

        if override_mode == "on":
            relay.on(1)
            lcd.status_ok("Manual: Motor ON")
            motor_on = True
        elif override_mode == "off":
            relay.off(1)
            lcd.error("Manual: Motor OFF")
            motor_on = False
        else:
            for step in plan:
                if "turn-on-motor" in step:
                    relay.on(1)
                    lcd.status_ok("Motor ON")
                    motor_on = True
                elif "turn-off-motor" in step:
                    relay.off(1)
                    lcd.error("Motor OFF")
                    motor_on = False
                elif "turn-on-fan" in step:
                    relay.on(2)
                    fan_on = True
                elif "turn-off-fan" in step:
                    relay.off(2)
                elif "emergency-stop-motor" in step:
                    relay.off(1)
                    lcd.error("Emergency Stop")

        # 8. If planner didn’t mention fan, turn it off
        if not any("fan" in step for step in plan):
            relay.off(2)

        # 9. Send updated state to dashboard via MQTT
        send_state_to_dashboard(state, plan, motor_on, fan_on)

        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting system.")
    relay.off(1)
    relay.off(2)
    lcd.display("System Halted")
    servo.cleanup()
