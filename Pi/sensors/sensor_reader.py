import time
import grovepi

DHT_SENSOR = 8
LIGHT_SENSOR = 0
PIR_SENSOR = 2
BUTTON = 3

class SensorReader:
    def __init__(self):
        grovepi.pinMode(PIR_SENSOR, "INPUT")
        grovepi.pinMode(BUTTON, "INPUT")
        self.last_dht = 0
        self.last_light = 0
        self.cached_temp = None
        self.cached_hum = None
        self.cached_light = None
        self.motion = None
        self.button = None

    def read_dht(self):
        current_time = time.time()
        if current_time - self.last_dht >= 15:
            for _ in range(3):
                try:
                    time.sleep(1.5)
                    temp, hum = grovepi.dht(DHT_SENSOR, 0)
                    if temp and hum and temp > 0 and hum > 0:
                        self.cached_temp = round(temp, 1)
                        self.cached_hum = round(hum, 1)
                        break
                except:
                    time.sleep(1)
            self.last_dht = current_time
        return self.cached_temp, self.cached_hum

    def read_light(self):
        current_time = time.time()
        if current_time - self.last_light >= 10:
            try:
                time.sleep(1)
                self.cached_light = grovepi.analogRead(LIGHT_SENSOR)
            except:
                self.cached_light = None
            self.last_light = current_time
        return self.cached_light

    def read_pir(self):
        try:
            time.sleep(0.1)
            self.motion = bool(grovepi.digitalRead(PIR_SENSOR))
        except:
            self.motion = False
        return self.motion

    def read_button(self):
        try:
            time.sleep(0.1)
            self.button = bool(grovepi.digitalRead(BUTTON))
        except:
            self.button = False
        return self.button

    def get_state(self):
        self.read_dht()
        self.read_light()
        self.read_pir()
        self.read_button()
        return {
            "temperature": self.cached_temp,
            "humidity": self.cached_hum,
            "light": self.cached_light,
            "motion": self.motion,
            "button_pressed": self.button
        }
