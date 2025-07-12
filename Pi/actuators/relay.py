######################################################################################################
# Authors : Susindhar Manivasagan, Raksha Nagendra, Mansi Sharad Dongare
######################################################################################################
# Modify address accordingly 
# actuator/relay.py

import smbus

class Relay:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.addr = 0x20     # Relay I2C address
        self.reg = 0x06      # Correct control register for your HAT
        self.data = 0xFF     # All OFF (active low)

        try:
            self.bus.write_byte_data(self.addr, self.reg, self.data)
        except Exception as e:
            print("Relay init failed:", e)

    def on(self, ch):
        self.data &= ~(0x1 << (ch - 1))
        self.bus.write_byte_data(self.addr, self.reg, self.data)

    def off(self, ch):
        self.data |= (0x1 << (ch - 1))
        self.bus.write_byte_data(self.addr, self.reg, self.data)
