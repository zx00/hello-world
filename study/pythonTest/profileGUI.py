import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QTimer
import subprocess
import re
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class AppMonitor(QWidget):
    def __init__(self):
        super(AppMonitor, self).__init__()

        self.device_id_label = QLabel('Device ID:')
        self.device_id_input = QLineEdit()
        self.package_name_label = QLabel('Package Name:')
        self.package_name_input = QLineEdit()
        self.start_button = QPushButton('Start Monitoring')
        self.end_button = QPushButton('End Monitoring')

        self.canvas = AppCanvas(self)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.device_id_label)
        input_layout.addWidget(self.device_id_input)
        input_layout.addWidget(self.package_name_label)
        input_layout.addWidget(self.package_name_input)
        input_layout.addWidget(self.start_button)
        input_layout.addWidget(self.end_button)

        button_layout = QHBoxLayout()
        button_layout.addLayout(input_layout)
        button_layout.addWidget(self.canvas)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_info)

        self.start_button.clicked.connect(self.start_monitoring)
        self.end_button.clicked.connect(self.end_monitoring)

    def start_monitoring(self):
        self.device_id = self.device_id_input.text()
        self.package_name = self.package_name_input.text()
        self.memory_data = []
        self.fps_data = []
        self.timer.start(1000)  # 更新间隔（毫秒）

    def end_monitoring(self):
        self.timer.stop()
        self.save_to_csv()

    def update_info(self):
        memory_usage = self.get_memory_usage()
        fps = self.get_fps()

        self.memory_data.append(memory_usage)
        self.fps_data.append(fps)

        print(f'存储内存值={self.memory_data}')

        self.canvas.plot(self.memory_data, self.fps_data)

    def get_memory_usage(self):
        result = subprocess.check_output(['adb', '-s', self.device_id, 'shell', 'dumpsys', 'meminfo', self.package_name]).decode('utf-8')
        print(f'内存={result},type={type(result)}')
        match = re.search(r'TOTAL PSS: +(\d+) ', result)
        print(f'内存2={match},type={type(match)}')
        if match:
            total_ram_kb = int(match.group(1))
            total_ram_mb = total_ram_kb / 1024
            print(f'内存值={total_ram_mb}')
            return total_ram_mb
        else:
            return 0

    def get_fps(self):
        result = subprocess.check_output(['adb', '-s', self.device_id, 'shell', 'dumpsys', 'gfxinfo', self.package_name]).decode('utf-8')
        print(f'FPS={result},type={type(result)}')
        match = re.search(r'Janky frames: (\d+)', result)
        print(f'FPS2={match},type={type(match)}')
        if match:
            janky_frames = int(match.group(1))
            total_frames = self.get_total_frames(result)
            fps = (total_frames - janky_frames) / total_frames * 60
            return round(fps, 2)
        else:
            return 0

    def get_total_frames(self, result):
        match = re.search(r'Total frames rendered: (\d+)', result, re.MULTILINE)
        if match:
            intervals_str = match.group(1)
            intervals = [int(interval) for interval in intervals_str.split()]
            return len(intervals)
        else:
            return 0

    def save_to_csv(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'monitor_data_{timestamp}.csv'

        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Timestamp', 'Memory (MB)', 'FPS'])

            for i in range(len(self.memory_data)):
                csv_writer.writerow([i + 1, self.memory_data[i], self.fps_data[i]])

        print(f'Data saved to {filename}')

class AppCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure()
        super(AppCanvas, self).__init__(self.figure)
        self.setParent(parent)

    def plot(self, memory_data, fps_data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.plot(memory_data, label='Memory (MB)')
        ax.plot(fps_data, label='FPS')

        ax.legend()
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Value')

        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    monitor = AppMonitor()
    monitor.show()
    sys.exit(app.exec_())
