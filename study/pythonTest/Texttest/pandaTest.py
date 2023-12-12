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
#使用glob获取指定目录下文件

def getFileListByGlob(dir:str,fileType:str):
    files=glob.glob(os.path.join(dir,f'*.{fileType}'))
    return files

def patterFile(path:dir,patter:str,fileType:str)->list:
    files=glob.glob(os.path.join(path,f'{patter}.{fileType}'))
    return files


def getnewDataForExecl(execlFile:str)->pd.DataFrame:
    #将数据转换为dataframe
    df=pd.DataFrame(pd.read_excel(execlFile))
    #填充空白
    new=df.fillna('空白')
    return new
# execlFile=EXECLFILE(os.path.join(dir,'111.xlsx'))
# df=pd.DataFrame(pd.read_excel(os.path.join(dir,'111.xlsx')))

# print(f'aa={df}')


# print(new)
# new.to_excel('new.xlsx')
# print(f'data11={new["状态"]},type={type(new["状态"])}')


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

# numPieList=getGroupByCloValue(new,'状态')

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

# createPie(numPieList,'严重程度分布')

#获取日期信息
def getDateGroup(df:pd.DataFrame,cloumName:str)->pd.DataFrame:
    #将对应列数据转换为datetime类型
    df[cloumName]=pd.to_datetime(df[cloumName])
    # 将日期列转换为周
    df['Week'] = df[cloumName].dt.to_period('W')
    #按照日期分组
    grouped=df.groupby(df[cloumName].dt.date)
    # for date,group in grouped:
    #     print(f'Date:{date}')
    #     print(f'Group:{group}')
    #     print('\n')
    # 按照周分组
    grouped = df.groupby('Week')

    # 遍历每个周分组并输出行数据
    for week, group in grouped:
        print(f"Week: {week}")
        print(group)
        print("\n")
        return grouped
if __name__=='__main__':
    #数据清洗
    #获取对应目录指定文件列表
    dir=os.path.dirname(os.path.abspath(__file__))
    fileType='xlsx'
    patter_str='111'
    file_list=patterFile(dir,patter_str,fileType)
    for f in file_list:
        #将空白填充为指定值
        #填充空白
        new=getnewDataForExecl(f)
        #按照日期进行分组展示
        # print(f'data={new}')
        #输出日期参数
        getDateGroup(new,'日期')

