import subprocess

result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
devices_info = [line.split('\t') for line in result.stdout.strip().split('\n')[1:]]
print(f'aa={result}')
print(f'qqq={devices_info}')