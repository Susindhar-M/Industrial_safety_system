import RPi.GPIO as GPIO
import threading
import time
from datetime import datetime
from rfid.MFRC522Custom import MFRC522Custom

READER_CONFIG = {
    "zone2": {"spi_dev": 0, "rst_pin": 22},  # Reader 1 (Zone 2 gate)
    "zone1": {"spi_dev": 1, "rst_pin": 18},  # Reader 2 (Zone 1 gate)
}

# Hardcoded tag-role mapping
TAG_ROLE_MAP = {
    "M1001": "M",
    "M1002": "M",
    "M1003": "M",
    "O4001": "O",
    "O4002": "O",
    "O4003": "O",
    "A1234": "A"
}

class RFIDManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.readers = {
            zone: MFRC522Custom(cfg["spi_dev"], cfg["rst_pin"])
            for zone, cfg in READER_CONFIG.items()
        }
        self.tag_tracker = {"zone1": set(), "zone2": set()}
        self.last_read_time = 0
        self.read_interval = 2
        self.log_file = "rfid/rfid_log.txt"

    def get_tag_type(self, tag_id):
        return TAG_ROLE_MAP.get(tag_id, None)

    def get_zone(self, tag):
        if tag in self.tag_tracker["zone1"]:
            return "zone1"
        if tag in self.tag_tracker["zone2"]:
            return "zone2"
        return "outside"

    def log_transition(self, tag, from_zone, to_zone):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} | {tag} | {from_zone} -> {to_zone}\n")

    def update_entry(self, tag, zone):
        current_zone = self.get_zone(tag)
        tag_type = self.get_tag_type(tag)

        if zone == "zone2":
            if current_zone == "outside":
                self.tag_tracker["zone2"].add(tag)
                self.log_transition(tag, "outside", "zone2")
            elif current_zone == "zone2":
                self.tag_tracker["zone2"].remove(tag)
                self.log_transition(tag, "zone2", "outside")
            elif current_zone == "zone1":
                self.tag_tracker["zone1"].remove(tag)
                self.tag_tracker["zone2"].add(tag)
                self.log_transition(tag, "zone1", "zone2")

        elif zone == "zone1":
            if tag_type != "M":
                self.log_transition(tag, "outside", "zone1 (DENIED)")
                return False

            if current_zone == "zone2":
                self.tag_tracker["zone2"].remove(tag)
                self.tag_tracker["zone1"].add(tag)
                self.log_transition(tag, "zone2", "zone1")
            elif current_zone == "zone1":
                self.tag_tracker["zone1"].remove(tag)
                self.tag_tracker["zone2"].add(tag)
                self.log_transition(tag, "zone1", "zone2")
            else:
                self.log_transition(tag, "outside", "zone1 (DENIED)")
                return False

        return True

    def get_state(self):
        return {
            "count1": len(self.tag_tracker["zone1"]),
            "count2": len(self.tag_tracker["zone2"])
        }

    def read_tags(self):
        current_time = time.time()
        if current_time - self.last_read_time < self.read_interval:
            return None

        for zone, reader in self.readers.items():
            with self.lock:
                (status, _) = reader.MFRC522_Request(reader.PICC_REQIDL)
                if status != reader.MI_OK:
                    continue

                (status, uid) = reader.MFRC522_Anticoll()
                if status != reader.MI_OK:
                    continue

                reader.MFRC522_SelectTag(uid)
                key = [0xFF] * 6
                block = 8

                if reader.MFRC522_Auth(reader.PICC_AUTHENT1A, block, key, uid) != reader.MI_OK:
                    continue

                data = reader.MFRC522_Read(block)
                reader.MFRC522_StopCrypto1()

                if data:
                    tag_id = bytearray(data).decode("utf-8").strip()
                    self.last_read_time = current_time
                    return {"tag": tag_id, "zone": zone}

        return None
