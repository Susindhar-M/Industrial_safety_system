######################################################################################################
# Authors : Susindhar Manivasagan, Raksha Nagendra, Mansi Sharad Dongare
######################################################################################################
# Do not modify
# actuator/lcd_display.py

from grove_rgb_lcd import setText, setRGB

class LCD:
    def __init__(self):
        setRGB(0, 128, 255)
        setText("LCD Ready")

    def display(self, text):
        # Trim or pad to fit 16x2
        lines = text.split("\n")
        if len(lines) == 1:
            setText(lines[0][:16] + "\n")
        else:
            setText(lines[0][:16] + "\n" + lines[1][:16])

    def error(self, msg="Error"):
        setRGB(255, 0, 0)
        self.display(msg)

    def status_ok(self, msg="OK"):
        setRGB(0, 255, 0)
        self.display(msg)

    def reset_color(self):
        setRGB(0, 128, 255)
