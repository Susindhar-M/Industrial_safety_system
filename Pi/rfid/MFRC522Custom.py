######################################################################################################
# Authors : Susindhar Manivasagan, Raksha Nagendra, Mansi Sharad Dongare
######################################################################################################
# Do not modify
# rfid/MFRC522Custom.py

# Library to read 2 rfids at the same time

import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import spidev
import logging

class MFRC522Custom(MFRC522):
    def __init__(self, dev, rst_pin):
        self.dev = dev
        self.spi = spidev.SpiDev()
        self.spi.open(0, dev)             # CE0 or CE1
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0
        self.RST = rst_pin

        # Set up logger
        self.logger = logging.getLogger(f"MFRC522-{dev}")
        self.logger.setLevel(logging.ERROR)  # Or DEBUG for more detail
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
            self.logger.addHandler(ch)

        # Setup RST pin
        GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.RST, GPIO.OUT)
        GPIO.output(self.RST, 1)

        self.MFRC522_Init()

    def cleanup(self):
        self.spi.close()
        GPIO.output(self.RST, 0)
