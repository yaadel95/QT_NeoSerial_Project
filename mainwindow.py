# This Python file uses the following encoding: utf-8
import sys
import time
import csv
from datetime import datetime

from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                              QWidget, QVBoxLayout, QHBoxLayout, QFileDialog)
from PySide6.QtCore import (Qt, QTimer, Property, QRect, QEasingCurve,
                           QPropertyAnimation)
from PySide6.QtGui import (QPainter, QColor, QPalette, QBrush, QPen,
                          QRadialGradient, QFontDatabase, QFont)

import serial as serial
import serial.tools.list_ports

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow


# Custom glowing indicator widget
class GlowIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._connected = False
        self._glow_color = QColor(0, 243, 255)
        self.setFixedSize(20, 20)

    def isConnected(self):
        return self._connected
    
    def setConnected(self, value):
        self._connected = value
        self.update()
        
    connected = Property(bool, isConnected, setConnected)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw main circle
        painter.setBrush(QBrush(self._glow_color if self._connected else QColor(42, 42, 74)))
        painter.setPen(QPen(QColor(42, 42, 74), 2))
        painter.drawEllipse(2, 2, 16, 16)
        
        # Draw glow effect
        if self._connected:
            gradient = QRadialGradient(10, 10, 10)
            gradient.setColorAt(0, QColor(0, 243, 255, 150))
            gradient.setColorAt(1, QColor(0, 243, 255, 0))
            painter.setBrush(QBrush(gradient))
            painter.drawEllipse(0, 0, 20, 20)
    
    

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.data_log = []


        # Custom initialization
        self.serial_port = None
        self.connected = False
        self.receive_buffer = ""
        
        # Setup custom UI elements
        self.setup_custom_widgets()
        self.setup_animations()
        self.apply_styles()
        self.setup_connections()
        self.refresh_ports()
        
        # Configure baudrates
        self.ui.cb_baudrate.addItems(['9600', '19200', '38400', '57600', '115200'])
        self.ui.cb_baudrate.setCurrentText('115200')
        
        # Setup serial read timer
        self.receive_timer = QTimer(self)
        self.receive_timer.timeout.connect(self.read_serial)
        
        # Set window properties
        self.setWindowTitle("NeoSerial")
        self.setGeometry(100, 100, 800, 600)

    def setup_custom_widgets(self):
        # Load custom font
        QFontDatabase.addApplicationFont("fonts/Orbitron-VariableFont_wght.ttf")
        
        # Set application font
        self.setFont(QFont("Orbitron", 10))        
        # Replace default indicator with our custom widget
        self.indicator = GlowIndicator()
        self.ui.horizontalLayout_3.replaceWidget(self.ui.indicator, self.indicator)
        self.ui.indicator.deleteLater()
        

    def apply_styles(self):
        self.setStyleSheet(open("styles.qss").read())
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 10, 18))
        palette.setColor(QPalette.WindowText, QColor(0, 243, 255))
        self.setPalette(palette)

    def setup_animations(self):
        # Setup animations for buttons
        for btn in [self.ui.btn_connect, self.ui.btn_refresh, 
                    self.ui.btn_send, self.ui.btn_clear]:
            btn.setCursor(Qt.PointingHandCursor)
            animation = QPropertyAnimation(btn, b"geometry")
            animation.setDuration(200)
            animation.setEasingCurve(QEasingCurve.OutBack)
            
            btn.enterEvent = lambda e, b=btn: self.animate_button(b, 1.05)
            btn.leaveEvent = lambda e, b=btn: self.animate_button(b, 1.0)

    def animate_button(self, button, scale):
        anim = QPropertyAnimation(button, b"geometry")
        anim.setDuration(200)
        anim.setEasingCurve(QEasingCurve.OutBack)
        current = button.geometry()
        anim.setStartValue(current)
        anim.setEndValue(QRect(
            current.x() - int((current.width() * (scale - 1)) / 2),
            current.y() - int((current.height() * (scale - 1)) / 2),
            int(current.width() * scale),
            int(current.height() * scale)
        ))
        anim.start()

    def setup_connections(self):
        self.ui.btn_connect.clicked.connect(self.toggle_connection)
        self.ui.btn_refresh.clicked.connect(self.refresh_ports)
        self.ui.btn_send.clicked.connect(self.send_data)
        self.ui.txt_send.returnPressed.connect(self.send_data)
        self.ui.btn_clear.clicked.connect(self.clear_received)
        self.ui.btn_save_csv.clicked.connect(self.save_to_csv)

    def refresh_ports(self):
        self.ui.cb_port.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.ui.cb_port.addItem(port.device)

    def toggle_connection(self):
        if not self.connected:
            self.connect_to_serial()
        else:
            self.disconnect_serial()

    def connect_to_serial(self):
        port = self.ui.cb_port.currentText()
        baudrate = int(self.ui.cb_baudrate.currentText())
        
        if not port:
            QMessageBox.warning(self, 'Warning', 'Please select a port!')
            return
            
        try:
            self.serial_port = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=0.1
            )
            self.connected = True
            self.ui.btn_connect.setText("DISCONNECT")
            self.receive_timer.start(50)
            self.indicator.connected = True
            QMessageBox.information(self, 'Connected', f'Successfully connected to {port}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
            self.connected = False
            self.indicator.connected = False

    def disconnect_serial(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.connected = False
        self.receive_timer.stop()
        self.ui.btn_connect.setText("CONNECT")
        self.indicator.connected = False
        QMessageBox.information(self, 'Disconnected', 'Serial connection closed')

    def log_data(self, data_type, data):
        """Log data with timestamp"""
        timestamp = datetime.now().isoformat(sep=' ', timespec='milliseconds')
        self.data_log.append({
            'timestamp': timestamp,
            'type': data_type,
            'data': data
        })
        
    def save_to_csv(self):
        if not self.data_log:
            QMessageBox.warning(self, 'Warning', 'No data to save!')
            return

        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save CSV File", "", 
            "CSV Files (*.csv)", 
            options=options
        )

        if filename:
            try:
                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = ['timestamp', 'type', 'data']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.data_log)
                QMessageBox.information(self, 'Success', 'Data saved successfully!')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save file: {str(e)}')

    def send_data(self):
        if not self.connected:
            QMessageBox.warning(self, 'Warning', 'Not connected to any device!')
            return
            
        data = self.ui.txt_send.text()
        if data:
            try:
                self.serial_port.write(f"{data}\n".encode())
                self.log_data('SENT', data)  # Log sent data
                self.ui.txt_send.clear()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f"Send failed: {str(e)}")
                self.disconnect_serial()

    def read_serial(self):
        if self.connected and self.serial_port:
            try:
                while self.serial_port.in_waiting > 0:
                    char = self.serial_port.read().decode('utf-8', errors='replace')
                    if char == '\n' or char == '\r':
                        if self.receive_buffer:
                            self.ui.txt_receive.append(f"[RECV] {self.receive_buffer}")
                            self.log_data('RECEIVED', self.receive_buffer)  # Log received data
                            self.receive_buffer = ""
                    else:
                        self.receive_buffer += char
            except Exception as e:
                QMessageBox.critical(self, 'Error', f"Read error: {str(e)}")
                self.disconnect_serial()


    def clear_received(self):
        self.ui.txt_receive.clear()
        self.data_log = []  # Clear log when user requests

    def closeEvent(self, event):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
