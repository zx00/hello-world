'''
以下是一个使用PyQt和ADB创建展示应用内存、FPS、CPU使用情况的脚本。该脚本允许用户输入设备ID、应用包名，并使用多选按钮选择获取内存、FPS、CPU使用情况中的哪些数据。
每个选择的数据类型都会在右侧创建一个独立的实时折线图。点击“开始监控”按钮后，实时折线图会开始更新，点击“结束监控”按钮后，数据会保存到CSV文件中。

确保你已经安装了PyQt5、Matplotlib和psutil，可以使用以下命令进行安装：

bash
Copy code
pip install PyQt5 matplotlib psutil


'''




import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from PyQt5.QtCore import Qt, QTimer
import subprocess
import re
import csv
from datetime import datetime
import psutil
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
        self.memory_checkbox = QCheckBox('Memory')
        self.fps_checkbox = QCheckBox('FPS')
        self.cpu_checkbox = QCheckBox('CPU')
        self.start_button = QPushButton('Start Monitoring')
        self.end_button = QPushButton('End Monitoring')

        self.figures = []
        self.canvases = []

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.device_id_label)
        input_layout.addWidget(self.device_id_input)
        input_layout.addWidget(self.package_name_label)
        input_layout.addWidget(self.package_name_input)
        input_layout.addWidget(self.memory_checkbox)
        input_layout.addWidget(self.fps_checkbox)
        input_layout.addWidget(self.cpu_checkbox)
        input_layout.addWidget(self.start_button)
        input_layout.addWidget(self.end_button)

        button_layout = QVBoxLayout()
        button_layout.addLayout(input_layout)

        for _ in range(3):  # Create three figures
            figure = Figure()
            canvas = AppCanvas(figure)
            self.figures.append(figure)
            self.canvases.append(canvas)
            button_layout.addWidget(canvas)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_info)

        self.start_button.clicked.connect(self.start_monitoring)
        self.end_button.clicked.connect(self.end_monitoring)

    def start_monitoring(self):
        self.device_id = self.device_id_input.text()
        self.package_name = self.package_name_input.text()

        self.monitor_memory = self.memory_checkbox.isChecked()
        self.monitor_fps = self.fps_checkbox.isChecked()
        self.monitor_cpu = self.cpu_checkbox.isChecked()

        for canvas in self.canvases:
            canvas.clear_data()

        self.timer.start(1000)  # 更新间隔（毫秒）

    def end_monitoring(self):
        self.timer.stop()
        self.save_to_csv()

    def update_info(self):
        if self.monitor_memory:
            memory_usage = self.get_memory_usage()
            self.canvases[0].plot(memory_usage, 'Memory (MB)')

        if self.monitor_fps:
            fps = self.get_fps()
            self.canvases[1].plot(fps, 'FPS')

        if self.monitor_cpu:
            cpu_usage = self.get_cpu_usage()
            self.canvases[2].plot(cpu_usage, 'CPU Usage (%)')

    def get_memory_usage(self):
        result = subprocess.check_output(['adb', '-s', self.device_id, 'shell', 'dumpsys', 'meminfo', self.package_name]).decode('utf-8')
        match = re.search(r'Total RAM: +(\d+) kB', result)
        if match:
            total_ram_kb = int(match.group(1))
            total_ram_mb = total_ram_kb / 1024
            return total_ram_mb
        else:
            return 0

    def get_fps(self):
        result = subprocess.check_output(['adb', '-s', self.device_id, 'shell', 'dumpsys', 'gfxinfo', self.package_name]).decode('utf-8')
        match = re.search(r'Janky frames: (\d+)/', result)
        if match:
            janky_frames = int(match.group(1))
            total_frames = self.get_total_frames(result)
            fps = (total_frames - janky_frames) / total_frames * 60
            return round(fps, 2)
        else:
            return 0

    def get_total_frames(self, result):
        match = re.search(r'Frame intervals in ms: (.+)$', result, re.MULTILINE)
        if match:
            intervals_str = match.group(1)
            intervals = [int(interval) for interval in intervals_str.split()]
            return len(intervals)
        else:
            return 0

    def get_cpu_usage(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        return cpu_percent

    def save_to_csv(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'monitor_data_{timestamp}.csv'

        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Timestamp', 'Memory (MB)', 'FPS', 'CPU Usage (%)'])

            for i in range(len(self.canvases[0].data)):
                csv_writer.writerow([i + 1, self.canvases[0].data[i], self.canvases[1].data[i], self.canvases[2].data[i]])

        print(f'Data saved to {filename}')

class AppCanvas(FigureCanvas):
    def __init__(self, figure, parent=None):
        super(AppCanvas, self).__init__(figure)
        self.setParent(parent)
        self.data_type_label = QLabel('')
        self.data = []

    def plot(self, value, data_type):
        self.data.append(value)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(self.data, label=data_type)
        ax.legend()
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Value')
        self.draw()

    def clear_data(self):
        self.data = []

if __name__ == '__main__':
    app = QApplication(sys.argv)
    monitor = AppMonitor()
    monitor.show()
    sys.exit(app.exec_())
