######################################################################################################
# Authors : Susindhar Manivasagan, Raksha Nagendra, Mansi Sharad Dongare
######################################################################################################
# Do not modify
# actuator/buzzer_led.py

# Importing libraries
import grovepi
import time

class BuzzerLED:
    def __init__(self):
        self.buzzer_pin = 6     # D6
        self.led_pins = {
            "zone1": 4,         # D4
            "zone2": 7          # D7
        }

        grovepi.pinMode(self.buzzer_pin, "OUTPUT")
        for pin in self.led_pins.values():
            grovepi.pinMode(pin, "OUTPUT")

    # LED and buzzer action for access granted
    def access_granted(self, zone="zone1"):
        # Short beep + LED zone of particular zone
        grovepi.digitalWrite(self.buzzer_pin, 1)
        grovepi.digitalWrite(self.led_pins.get(zone, 5), 1)
        time.sleep(0.2)
        grovepi.digitalWrite(self.buzzer_pin, 0)
        grovepi.digitalWrite(self.led_pins.get(zone, 5), 0)

    # LED and buzzer action for access denied
    def access_denied(self):
        # Repeated buzz 
        for _ in range(3):
            grovepi.digitalWrite(self.buzzer_pin, 1)            
            time.sleep(0.3)
            grovepi.digitalWrite(self.buzzer_pin, 0)            
            time.sleep(0.2)
