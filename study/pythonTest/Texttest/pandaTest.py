import pandas as pd
import re
import os
import glob
from matplotlib import pyplot as plt
import numpy as np


#获取同个目录下所有xls文件

def getDirFileList(dir:str):
    fileList=[]
    #获取所有文件列表
    files=os.listdir(dir)
    for file in files:
        #如果是指定路径下的文件，就添加到返回列表

        if os.path.isfile(os.path.join(dir,file)):
            fileList.append(file)
    return fileList

dir=r'F:\StudyTest\testPublic\hello-world\study\pythonTest\Texttest'
fileType='xlsx'
print(getDirFileList(dir))

#使用glob获取指定目录下文件

def getFileListByGlob(dir:str,fileType:str):
    files=glob.glob(os.path.join(dir,f'*.{fileType}'))
    return files

for i in getFileListByGlob(dir,fileType):
    #获取指定路径文件的文件名
    print(os.path.basename(i))
print(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())
def patterFile():
    files=glob.glob(os.path.join(dir,'缺陷情况*.xlsx'))
    print(f'a={files}')

patterFile()




def getDataForExecl(execlFile:str):
    #将数据转换为dataframe
    df=pd.DataFrame(pd.read_excel(execlFile))
#将execl内容封装为类
class EXECLFILE:

    def __init__(self,execlFile:str) -> None:
        self.pd=pd.read_excel(execlFile)
        self.df=pd.DataFrame(self.df)


# execlFile=EXECLFILE(os.path.join(dir,'111.xlsx'))
df=pd.DataFrame(pd.read_excel(os.path.join(dir,'111.xlsx')))

# print(f'aa={df}')

#填充空白
new=df.fillna('空白')
# print(new)
new.to_excel('new.xlsx')


print(f'data11={new["状态"]},type={type(new["状态"])}')


# print(f'状态={statList},type={type(statList)}')

# print(f'列名')
#获取对应列对应数据的行数据




#获取对应列所有信息，并且按照内容进行相应的筛选并生成对应execl

def getGroupByCloValue(newExecl:pd,cloName:str):
#状态列表
    statList=list(set(newExecl[cloName]))
    staDir={}
    for i in statList:
        staDir[i]=newExecl[newExecl[cloName]==i]
    for i,j in staDir.items():
        print(f'{cloName}为{i}的BUG数量:\t{len(j)}')
        j.to_excel(f'{cloName}为{i}的BUG情况.xlsx')
    return staDir

numPieList=getGroupByCloValue(new,'状态')

#饼状图数据

#生成柱状图

def createPie(data:dict,title:str):
    sizeList=[]
    labelList=[]
    for i,j in data.items():
        sizeList.append(len(j))
        labelList.append(i)
    # y=np.array(data)
    #饼图的标签
    #动态展示中文
    print(f'fff={sizeList}')
    print(f'aaa={labelList}')
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['font.family']='sans-serif'
    #绘制饼图
    plt.pie(sizeList,labels=labelList,autopct='%1.1f%%')
    #标题
    plt.title(title)
    plt.show()

totalNum=len(new)

print(f'new{totalNum}')

createPie(numPieList,'严重程度分布')