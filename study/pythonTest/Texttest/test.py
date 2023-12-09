import os
import subprocess
txt=os.system("dir")
print(f'a={txt}')
#执行shell指令

cmd='dir'

# da=subprocess.check_output(cmd,shell=True)
da=subprocess.run(cmd,shell=True,capture_output=True,encoding='gbk')
# a=da.splitlines()
# print(f'da={da}/nc={a}')
print(type(da))
print(f'aaaa={da}')