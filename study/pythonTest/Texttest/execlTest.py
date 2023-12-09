import xlrd

book=xlrd.open_workbook(r'F:\StudyTest\testPublic\hello-world\study\pythonTest\Texttest\111.xlsx')
# book1=xlrd.open_workbook(r'F:/StudyTest/testPublic/hello-world\study/pythonTest/Texttest/111.xlsx')
print(f'sheet={book.nsheets}')
sh=book.sheet_by_index(0)
print(sh.nrows)
print(type(sh.ncols))
#循环输出每一行内容
for i in range(sh.nrows):
    print(f'第{i+1}行内容是{sh.row_values(rowx=i)}')
#循环输出每一列内容
for i in range(sh.ncols):
    print(f'第{i+1}行内容是{sh.col_values(colx=i)}')
#模块名
mouds=sh.col_values(colx=0)

a=['A','C']
dic={}
#循环模块读取
for j in a:
    a=[]
    for index,i in enumerate(mouds):
        #如果属于此模块
        if i ==j:
            #抛出此数据
            a.append(index)
            print(f'a={a}moud={mouds}')
    dic[j]=a

print(f'dic={dic}')
for j in dic.values():
    print(j)
    if  j :
        print(f'j={j}')
        for a in j:
            print(sh.row_values(rowx=a))