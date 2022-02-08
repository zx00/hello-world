#读取文件使用 open() 方法一定要保证关闭文件对象，即调用 close() 方法。
#增加
#修改
#删除
context='hello,world'
f = open ("hello.txt","r+")
print (f.closed)
print (f.mode)
print (f.name)
f.write(context)
print ("write ok")
print (f.read())
f.close()
# 2 读取文件可以使用readline()函数、readlines()函数和read函数。
# 3 写入文件可以使用write()、writelines()函数