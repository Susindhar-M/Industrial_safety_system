######################################################################################################
# Authors : Susindhar Manivasagan, Raksha Nagendra, Mansi Sharad Dongare
######################################################################################################
# Modify pins accordingly 
# actuator/servo.py

import RPi.GPIO as GPIO
import time

class ServoController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.servo_pins = {
            "zone1": 17,  # GPIO17 (physical pin 11)
            "zone2": 27   # GPIO27 (physical pin 13)
        }

        self.pwms = {}
        for zone, pin in self.servo_pins.items():
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, 50)  # 50 Hz
            pwm.start(0)
            self.pwms[zone] = pwm

    # Rotate selected servo 90 degrees clockwise 
    def open(self, zone):
        if zone in self.pwms:
            self.pwms[zone].ChangeDutyCycle(6.6)  # open position
            time.sleep(0.5)
            self.pwms[zone].ChangeDutyCycle(0)

    # Rotate selected servo 90 degrees Anti-clockwise 
    def close(self, zone):
        if zone in self.pwms:
            self.pwms[zone].ChangeDutyCycle(7.8)  # closed position
            time.sleep(0.5)
            self.pwms[zone].ChangeDutyCycle(0)

    def cleanup(self):
        for pwm in self.pwms.values():
            pwm.stop()
        GPIO.cleanup()
