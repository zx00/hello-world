'''
下面是一个可以在当前已连接设备中选择一个并获取该设备所有应用的脚本。
脚本使用了 androidviewclient 库来获取应用信息，
同时使用了 matplotlib 进行实时折线图的展示。请确保你的设备已连接，
并且 adb 工具和 androidviewclient 库都已安装。

'''

import subprocess
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import threading
import time
import csv
import tkinter as tk
from tkinter import ttk
from androidviewclient import ViewClient

# 设置图形相关参数
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
line_cpu, = ax1.plot([], [], label='CPU Usage (%)')
line_memory, = ax2.plot([], [], label='Memory Usage (MB)')
line_fps, = ax3.plot([], [], label='FPS')
line_jank, = ax4.plot([], [], label='Jank Count')
ax1.set_xlim(0, 60)
ax1.set_ylim(0, 100)
ax2.set_xlim(0, 60)
ax2.set_ylim(0, 500)  # 设置合适的内存范围
ax3.set_xlim(0, 60)
ax3.set_ylim(0, 60)  # 设置合适的FPS范围
ax4.set_xlim(0, 60)
ax4.set_ylim(0, 10)  # 设置合适的Jank范围
ax1.set_ylabel('CPU Usage (%)')
ax2.set_ylabel('Memory Usage (MB)')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('FPS')
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Jank Count')

# CPU、内存、FPS、Jank、电量和流量情况数据
cpu_data = {'time': [], 'usage': []}
memory_data = {'time': [], 'usage': []}
fps_data = {'time': [], 'fps': []}
jank_data = {'time': [], 'count': []}

# 是否正在收集数据的标志
collecting_data = False

# 当前选择的应用信息
selected_app_info = None

# CSV文件相关参数
csv_file_path = 'performance_data.csv'
csv_file_header = ['Time', 'CPU Usage (%)', 'Memory Usage (MB)', 'FPS', 'Jank Count']

def get_connected_devices():
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    devices_info = [line.split('\t') for line in result.stdout.strip().split('\n')[1:]]
    return devices_info

def get_installed_apps(device_id):
    result = subprocess.run(["adb", "-s", device_id, "shell", "pm", "list", "packages", "-3"], capture_output=True, text=True)
    return [line.split(":")[1] for line in result.stdout.strip().split('\n')]

def get_app_info(device_id, app_package):
    vc = ViewClient(device_id)
    app_info = {}
    try:
        vc.dump()
        app_view = vc.findViewWithText(app_package)
        app_info['name'] = app_view.getText()
        app_info['icon'] = app_view.get('resource-id')
    except Exception as e:
        print(f"Error getting app info: {e}")
    return app_info

def start_collection():
    global collecting_data
    global selected_app_info
    collecting_data = True
    print(f"Starting performance data collection for app: {selected_app_info['name']}")

    # 创建CSV文件并写入表头
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(csv_file_header)

    # 启动收集数据线程
    collection_thread = threading.Thread(target=collect_data)
    collection_thread.start()

def stop_collection():
    global collecting_data
    collecting_data = False
    print("Stopping performance data collection.")

def collect_data():
    start_time = datetime.now()

    last_frame_time = 0
    frame_count = 0
    jank_count = 0

    while collecting_data:
        # 获取CPU使用情况
        result_cpu = subprocess.run(["adb", "shell", "top", "-n", "1", "-d", "1", "-m", "1", "-n", "1", "-s", "cpu", "-p", selected_app_info['name']], capture_output=True, text=True)
        cpu_line = result_cpu.stdout.split('\n')[2]
        cpu_usage = float(cpu_line.split()[2].replace('%', ''))

        # 获取内存使用情况
        result_memory = subprocess.run(["adb", "shell", "dumpsys", "meminfo", selected_app_info['name']], capture_output=True, text=True)
        memory_line = [line for line in result_memory.stdout.split('\n') if "TOTAL" in line][0]
        memory_usage = int(memory_line.split()[1]) / (1024 * 1024)  # 转换为MB

        # 获取FPS
        result_fps = subprocess.run(["adb", "shell", "dumpsys", "gfxinfo", selected_app_info['name']], capture_output=True, text=True)
        fps_line = [line for line in result_fps.stdout.split('\n') if "Janky frames" in line][0]
        fps = int(fps_line.split(':')[1].strip())

        # 计算Jank
        current_time = time.time() * 1000  # 毫秒
        frame_duration = current_time - last_frame_time
        last_frame_time = current_time

        if frame_duration > 16.6:
            jank_count += 1

        frame_count += 1
        if frame_count % 60 == 0:
            fps_data['time'].append(elapsed_time)
            fps_data['fps'].append(fps)
            frame_count = 0
            fps = 0

        # 更新图形数据
        elapsed_time = (datetime.now() - start_time).seconds
        cpu_data['time'].append(elapsed_time)
        cpu_data['usage'].append(cpu_usage)
        memory_data['time'].append(elapsed_time)
        memory_data['usage'].append(memory_usage)
        jank_data['time'].append(elapsed_time)
        jank_data['count'].append(jank_count)

        # 更新CSV文件
        with open(csv_file_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([elapsed_time, cpu_usage, memory_usage, fps, jank_count])

        line_cpu.set_data(cpu_data['time'], cpu_data['usage'])
        line_memory.set_data(memory_data['time'], memory_data['usage'])
        line_fps.set_data(fps_data['time'], fps_data['fps'])
        line_jank.set_data(jank_data['time'], jank_data['count'])

        # 更新X轴范围，保持窗口显示最近60秒的数据
        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_xlim(max(0, elapsed_time - 60), elapsed_time + 5)

        time.sleep(1)

    print("Data collection thread stopped.")

def on_device_selected(event):
    global selected_device_id
    selected_device_id = device_combobox.get()
    update_app_list()

def on_app_selected(event):
    global selected_app_info
    selected_app_info = app_combobox.get()
    app_info = get_app_info(selected_device_id, selected_app_info)
    app_name_label.config(text=f"Selected App: {app_info['name']}")
    app_icon_label.config(text=f"Icon: {app_info['icon']}")

def update_app_list():
    device_id = device_combobox.get()
    apps = get_installed_apps(device_id)
    app_combobox['values'] = apps
    app_combobox.current(0)  # 默认选择第一个应用
    on_app_selected(None)  # 更新应用信息

# 获取连接设备信息
devices_info = get_connected_devices()
device_ids = [device_info[0] for device_info in devices_info]

# 创建主窗口
root = tk.Tk()
root.title("App Performance Monitor")

# 显示连接的设备信息
device_label = tk.Label(root, text="Connected Devices:")
device_label.pack()

# 创建设备选择下拉框
device_combobox = ttk.Combobox(root, values=device_ids)
device_combobox.pack()
device_combobox.bind("<<ComboboxSelected>>", on_device_selected)

# 显示选择的设备信息
selected_device_id = device_combobox.get()
selected_device_label = tk.Label(root, text=f"Selected Device: {selected_device_id}")
selected_device_label.pack()

# 显示连接设备上的所有应用
app_label = tk.Label(root, text="Select an app:")
app_label.pack()

# 创建应用选择下拉框
app_combobox = ttk.Combobox(root, values=get_installed_apps(selected_device_id))
app_combobox.pack()
app_combobox.bind("<<ComboboxSelected>>", on_app_selected)

# 显示选择的应用信息
app_name_label = tk.Label(root, text="Selected App: ")
app_name_label.pack()

app_icon_label = tk.Label(root, text="Icon: ")
app_icon_label.pack()

# 添加开始和结束按钮
start_button = tk.Button(root, text="Start", command=start_collection, bg='green', fg='white')
start_button.pack(side=tk.LEFT, padx=5)
end_button = tk.Button(root, text="End", command=stop_collection, bg='red', fg='white')
end_button.pack(side=tk.LEFT, padx=5)

# 显示图形
plt.show()

# 运行主循环
root.mainloop()