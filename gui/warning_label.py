# i wanted to be able to set all of these properties from QtDesigner but I can't get them to show up, so this isn't used
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtProperty, Qt

class WarningLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._min_val = 0
        self._max_val = 100
        self._red_high = True
        self._display_float = False

    @pyqtProperty(int, designable=True)
    def min_val(self):
        return self._min_val

    @min_val.setter
    def min_val(self, value):
        self._min_val = value

    @pyqtProperty(int, designable=True)
    def max_val(self):
        return self._max_val

    @max_val.setter
    def max_val(self, value):
        self._max_val = value

    @pyqtProperty(bool, designable=True)
    def red_high(self):
        return self._red_high

    @red_high.setter
    def red_high(self, value):
        self._red_high = value

    @pyqtProperty(bool, designable=True)
    def display_float(self):
        return self._display_float

    @display_float.setter
    def display_float(self, value):
        self._display_float = value

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def set_value(self, value):
        # Clamp the value within the min and max range
        value = max(self.min_val, min(self.max_val, value))
        # Normalize the value to a range of 0 to 1
        normalized_value = (value - self.min_val) / (self.max_val - self.min_val)
        # Interpolate the hue value
        hue = normalized_value * 101 if self.red_high else (1 - normalized_value) * 101
        # Set the color based on the hue
        color = QColor.fromHsv(hue, 240, 240)
        # Apply the color to the label's stylesheet
        self.setStyleSheet(f"background-color: {color.name()};")
        # Set the label's text
        self.setText(f"{value:.1f}" if self.display_float else f"{int(value)}")

# Usage in PyQt Designer:
# 1. Create a QLabel in the PyQt Designer.
# 2. Right-click the QLabel and select 'Promote to...'.
# 3. In the 'Promoted class name' field, enter 'ColorInterpolatingLabel'.
# 4. In the 'Header file' field, enter the name of your Python file containing the class (e.g., 'my_label.py').
# 5. Click 'Add' and then 'Promote'.
# 6. In your Python code, you can now set the properties of the label like this:
# label = ColorInterpolatingLabel(min_val=0, max_val=100, red_high=False, display_float=True)
# label.set_value(50.5)  # Set this to the numerical value you want to display

# Usage in PyQt Designer:
# 1. Promote the QLabel to ColorInterpolatingLabel as described previously.
# 2. After promotion, the properties min_val, max_val, red_high, and display_float will appear in the Property Editor where you can set their values.