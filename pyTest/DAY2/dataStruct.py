#元组 tuple 类似无法修改的数组 不同元素
tuple_name =('apple','banana','grape','orange')

#1.查看
print (tuple_name[0])
print (tuple_name[0:3])
#2.增加
#3.修改
tup1=(1,"aaa")
tup2=("bb",22)
#元组无法修改
# tup1[0]=521
print (tup1+tup2)
#4.删除
# 元素无法删除，只能删除元组
del tup1
# print (tup1)


#列表 list 类型数组 相同元素 可修改 remove append
list =['apple','banana','grage','orange']
#循环遍历
def allList(list):
    for i in range(len(list)) :
        print (list[i])
#2.1增加
# allList(list)
list.append('1')
# allList(list)
#2.2删除元素 del
print (list)
del list[1]
print(list)
#2.3修改元素
# allList(list)
list[0]='a'
# allList(list)
#2.4读取元素
print (list[0])
print (list[1:3])
#字典 键值对 
dict ={"a":"aa"}