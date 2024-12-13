from PyQt5.QtWidgets import QCheckBox

class ClickableCheckBox(QCheckBox):
    def mouseReleaseEvent(self, event):
        # Toggle the checkbox when clicked anywhere inside the widget
        self.setChecked(not self.isChecked())
        super().mousePressEvent(event)

    def changeEvent(self,evt):
        pass


from PyQt5.QtWidgets import (
    QDial, QLabel, QStackedLayout, QWidget, QInputDialog, QApplication
)
from PyQt5.QtCore import Qt, QTimer, QElapsedTimer


class CustomDial(QWidget):
    def __init__(self, name = '', min_value=0.0, max_value=100.0, initial_value=50.0, parent=None):
        super().__init__(parent)
        
        self.dial = QDial()
        self.dial.setRange(0, 1000)  # Use an integer range for internal precision
        self.dial.setValue(int((initial_value - min_value) / (max_value - min_value) * 1000))
        
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = initial_value
        
        self.name_label = QLabel(f"{name}")
        self.name_label.setAlignment(Qt.AlignTop)
        self.name_label.setStyleSheet("font-size: 12px; background: none;")

        self.value_label = QLabel(f"{initial_value:.2f}")
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("font-size: 18px; font-weight: bold; background: none;")
        
        self.layout = QStackedLayout(self)
        self.layout.addWidget(self.dial)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.value_label)
        
        self.dial.valueChanged.connect(self.update_label)
        
        self.drag_start_position = None
        self.is_dragging = False
        self.timer = QElapsedTimer()

    def update_label(self, value):
        """Update the label when the dial value changes."""
        self.current_value = self.min_value + (value / 1000) * (self.max_value - self.min_value)
        self.value_label.setText(f"{self.current_value:.2f}")
    
    def mouseReleaseEvent(self, event):
        """Stop tracking drag movements and check for quick release."""
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            duration = self.timer.elapsed()
            if duration < 300:  # Quick release within 0.3 seconds
                delta = event.pos() - self.drag_start_position
                if abs(delta.x()) < 10 and abs(delta.y()) < 10:
                    self.open_set_value_dialog()
        super().mouseReleaseEvent(event)
    
    def open_set_value_dialog(self):
        """Open a dialog to set an exact value."""
        value, ok = QInputDialog.getDouble(
            self, "Set Value", "Enter a value:", self.current_value,
            self.min_value, self.max_value, decimals=2
        )
        if ok:
            self.current_value = value
            # Update the dial to match the new value
            self.dial.setValue(int((value - self.min_value) / (self.max_value - self.min_value) * 1000))
            self.update_label(self.dial.value())
