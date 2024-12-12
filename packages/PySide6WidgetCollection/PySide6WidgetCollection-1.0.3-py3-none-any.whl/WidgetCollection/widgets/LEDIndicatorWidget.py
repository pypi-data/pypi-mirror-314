import PySide6
from PySide6.QtWidgets import QLabel

class LEDIndicatorWidget(QLabel):
    def __init__(self, color="yellow"):
        super().__init__()
        self.size = 8
        self._create_led(color)

    def _create_led(self, color):
        self.set_color(color)

    def set_color(self, color):
        self.setStyleSheet(
            "QLabel {background-color : " f"{color};"
            "border-color : black; "
            "border-width: 1px; "
            "border-style: solid; "
            f"border-radius: {int(self.size / 2)}px; "
            f"min-height: {self.size}px; "
            f"min-width: {self.size}px; "
            f"max-height: {self.size}px; "
            f"max-width: {self.size}px"
            "}")
