'''

下面是一个综合了CPU、内存、Jank、电量和流量情况的 Python 脚本示例。
这个脚本会在实时折线图上显示这些性能数据，并提供开始和结束功能，
同时还会展示连接的设备信息。请确保你的电脑上已经安装了 matplotlib 库。
'''
import subprocess
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import threading
import time
import csv

# 设置应用包名
app_package = "com.winner.metaapp"

# 设置图形相关参数
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
line_cpu, = ax1.plot([], [], label='CPU Usage (%)')
line_memory, = ax2.plot([], [], label='Memory Usage (MB)')
line_jank, = ax3.plot([], [], label='Jank Count')
line_battery, = ax4.plot([], [], label='Battery Level (%)')
ax1.set_xlim(0, 60)
ax1.set_ylim(0, 100)
ax2.set_xlim(0, 60)
ax2.set_ylim(0, 500)  # 设置合适的内存范围
ax3.set_xlim(0, 60)
ax3.set_ylim(0, 10)  # 设置合适的Jank范围
ax4.set_xlim(0, 60)
ax4.set_ylim(0, 100)  # 设置合适的电量范围
ax1.set_ylabel('CPU Usage (%)')
ax2.set_ylabel('Memory Usage (MB)')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Jank Count')
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Battery Level (%)')

# CPU、内存、Jank、电量和流量情况数据
cpu_data = {'time': [], 'usage': []}
memory_data = {'time': [], 'usage': []}
jank_data = {'time': [], 'count': []}
battery_data = {'time': [], 'level': []}

# 是否正在收集数据的标志
collecting_data = False

# CSV文件相关参数
csv_file_path = 'performance_data.csv'
csv_file_header = ['Time', 'CPU Usage (%)', 'Memory Usage (MB)', 'Jank Count', 'Battery Level (%)']

def get_connected_devices():
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    devices_info = [line.split('\t') for line in result.stdout.strip().split('\n')[1:]]
    return devices_info

def start_collection():
    global collecting_data
    collecting_data = True
    print("Starting performance data collection.")

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

    while collecting_data:
        # 获取连接设备信息
        devices_info = get_connected_devices()
        print("Connected Devices:")
        for device_info in devices_info:
            print(f"Device: {device_info[0]}, Status: {device_info[1]}")
             # 获取内存使用情况
        result_memory = subprocess.run(["adb", "-s",f"{devices_info[0][0]}","shell", "dumpsys", "meminfo", app_package], capture_output=True, text=True)
        memory_line = [line for line in result_memory.stdout.split('\n') if "TOTAL" in line][0]
        memory_usage = int(memory_line.split()[1]) / (1024 * 1024)  # 转换为MB

        # 获取CPU使用情况
        #获取PID
        app_PID=subprocess.run(["adb","-s" ,devices_info[0][0], "shell","pidof",app_package],capture_output=True,text=True)
        print(f'qqqqq={app_PID.stdout.strip()}')
        # result_cpu = subprocess.run(["adb", "-s",devices_info[0][0],"shell", "top", "-n", "1", "-d", "1", "-m", "1" , "-s", "cpu","-p",app_PID], capture_output=True, text=True)
        result_cpu = subprocess.run(["adb", "-s",devices_info[0][0],"shell", "top", "-n", "1", "-d", "1", "-m", "1" ,"-p",f'{app_PID.stdout.strip()}'], capture_output=True, text=True)
        print(f'res={result_cpu}')
        cpu_line = result_cpu.stdout.split('\n')[2]
        cpu_usage = float(cpu_line.split()[2].replace('%', ''))

        # # 获取内存使用情况
        # result_memory = subprocess.run(["adb", "shell", "dumpsys", "meminfo", app_package], capture_output=True, text=True)
        # memory_line = [line for line in result_memory.stdout.split('\n') if "TOTAL" in line][0]
        # memory_usage = int(memory_line.split()[1]) / (1024 * 1024)  # 转换为MB

        # 获取Jank情况
        result_jank = subprocess.run(["adb", "shell", "dumpsys", "gfxinfo", app_package], capture_output=True, text=True)
        jank_count_line = [line for line in result_jank.stdout.split('\n') if "Jank" in line][0]
        jank_count = int(jank_count_line.split()[-1])

        # 获取电池电量
        result_battery = subprocess.run(["adb", "shell", "dumpsys", "battery", "--current"], capture_output=True, text=True)
        battery_level_line = [line for line in result_battery.stdout.split('\n') if "level" in line][0]
        battery_level = int(battery_level_line.split(':')[1].strip())

        # 更新图形数据
        elapsed_time = (datetime.now() - start_time).seconds
        cpu_data['time'].append(elapsed_time)
        cpu_data['usage'].append(cpu_usage)
        memory_data['time'].append(elapsed_time)
        memory_data['usage'].append(memory_usage)
        jank_data['time'].append(elapsed_time)
        jank_data['count'].append(jank_count)
        battery_data['time'].append(elapsed_time)
        battery_data['level'].append(battery_level)

        # 更新CSV文件
        with open(csv_file_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([elapsed_time, cpu_usage, memory_usage, jank_count, battery_level])

        line_cpu.set_data(cpu_data['time'], cpu_data['usage'])
        line_memory.set_data(memory_data['time'], memory_data['usage'])
        line_jank.set_data(jank_data['time'], jank_data['count'])
        line_battery.set_data(battery_data['time'], battery_data['level'])

        # 更新X轴范围，保持窗口显示最近60秒的数据
        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_xlim(max(0, elapsed_time - 60), elapsed_time + 5)

        time.sleep(1)

    print("Data collection thread stopped.")

# 添加开始和结束按钮
start_button = plt.axes([0.8, 0.01, 0.1, 0.05])
end_button = plt.axes([0.91, 0.01, 0.1, 0.05])

start_button_obj = plt.Button(start_button, 'Start', color='green', hovercolor='0.975')
end_button_obj = plt.Button(end_button, 'End', color='red', hovercolor='0.975')

start_button_obj.on_clicked(lambda event: start_collection())
end_button_obj.on_clicked(lambda event: stop_collection())

# 显示图形
plt.show()
