#格式化输出
format ="%s%d" % ("a",2)
print (format)
#增加
str1='hello'
str2='world'
result=str1+str2
print (result)
#字符串截取（切片）
word='world'
print (word[0:3])

#字符串比较
# python使用==和!=来进行字符串比较。如果比较的两个变量的类型不相同，那么结果必然为不同
s1='test1'
s2='test2'
s3='test1'
print (s1==s2)
print (s1!=s2)
print (s1==s3)
print (s1!=s3)

#字符串格式化
print('今年%s已经%d岁了'%('张三',10))
