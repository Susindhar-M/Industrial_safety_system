import time
import os

class OccupancyManager:
    def __init__(self, log_file="logs/occupancy_log.txt"):
        self.zone1 = set()
        self.zone2 = set()
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def is_access_allowed(self, tag_type, scanned_zone):
        if scanned_zone == "zone1":
            return tag_type == "M" and tag_type is not None and \
                   tag_type.upper() == "M" and \
                   len(self.zone1) < 1 and \
                   (tag_type in self.zone2 or tag_type in self.zone1)
        elif scanned_zone == "zone2":
            return tag_type in ["M", "O"]
        return False

    def update_entry(self, tag_id, scanned_zone):
        from_zone = self.get_zone(tag_id)
        to_zone = None

        # Reader 1 logic (Zone 2)
        if scanned_zone == "zone2":
            if tag_id in self.zone1:
                # Exit from Zone 1 to Zone 2
                self.zone1.remove(tag_id)
                self.zone2.add(tag_id)
                to_zone = "zone2"
            elif tag_id in self.zone2:
                # Exit system
                self.zone2.remove(tag_id)
                to_zone = "outside"
            else:
                # Entry to Zone 2
                self.zone2.add(tag_id)
                to_zone = "zone2"

        # Reader 2 logic (Zone 1)
        elif scanned_zone == "zone1":
            if tag_id in self.zone2:
                # Entry to Zone 1
                self.zone2.remove(tag_id)
                self.zone1.add(tag_id)
                to_zone = "zone1"
            elif tag_id in self.zone1:
                # Exit to Zone 2
                self.zone1.remove(tag_id)
                self.zone2.add(tag_id)
                to_zone = "zone2"

        if to_zone:
            self._log_movement(tag_id, from_zone, to_zone)

    def get_zone(self, tag_id):
        if tag_id in self.zone1:
            return "zone1"
        elif tag_id in self.zone2:
            return "zone2"
        return "outside"

    def _log_movement(self, tag_id, from_zone, to_zone):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} | {tag_id} | {from_zone} -> {to_zone}\n")

    def get_state(self):
        return {
            "zone1": list(self.zone1),
            "zone2": list(self.zone2),
            "count1": len(self.zone1),
            "count2": len(self.zone2)
        }
