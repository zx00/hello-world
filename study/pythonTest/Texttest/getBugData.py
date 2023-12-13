import pandas as pd
import re
import os
import glob
from pandas import DataFrame as df
from matplotlib import pyplot as plt


#获取指定路径所有符合匹配的相应模式的文件
def getPatterFileList(dir:str,patter:re,fileType:str)->list:
    fileList=glob.glob(os.path.join(dir,f'{patter}.{fileType}'))

    return fileList
def getExeclDataNotNan(execl_dir:str,nanStr:str)->df:
    df=pd.read_excel(execl_dir)
    new=df.fillna(nanStr)
    return new
#对某一列数据进行分组获得
def getGroupDataByallValues(new:df,clou_name:str)->df:
    result=new.groupby(clou_name)
    return result
#对分组后的数据获取对应分组的总行数,并且用df存储
def getNumByGroup(group:df.groupby)->df:
    moudl_list=[]
    num_list=[]
    for name,group in group:
        print(f'name={name}type={type(name)}')
        print(f'groupType={type(group)}"\n"grouplen={len(group)}"\n"group={group}')
        print('\n')
        #存储对应分组数据
        moudl_list.append(name)
        num_list.append(len(group))
        data={
            'moudleName':moudl_list,
            'sum':num_list
        }
    df=pd.DataFrame(data)
    return df
#饼图展示
def getPieData(new:df,title:str):

    plt.pie(new['moudleName'],new['sum'])
    plt.show()
    pass
#生成柱状图展示,在每个柱状体上面显示对应数量
def getBarData(new:df,title:str):
    moudl_list=new['moudleName']
    sum_list=new['sum']
    plt.bar(moudl_list,sum_list)
    # 在每个柱状体上方添加数字
    for i, value in enumerate(sum_list):
        plt.text(i, value + 1, str(value), ha='center', va='bottom')
    #添加标题
    plt.title=title
    plt.show()
    pass
#生成折线图图展示,在每个折线上面显示对应数量
def getPlotData(new:df,title:str):
    
    y_values=new['sum']
    x_values=[i for i in range(len(y_values))]
    plt.plot(x_values,y_values)

    # 在每个折线上方添加数字
    for x, y1 in zip(x_values,y_values):
        plt.text(x, y1 + 1, str(y1), ha='center', va='bottom', color='blue')
        # plt.text(x, y2 - 1, str(y2), ha='center', va='top', color='orange')
    
    #添加标题
    plt.title=title
    plt.xlabel('X轴')
    plt.ylabel('Y轴')

    # 显示图例
    plt.legend()

    plt.show()
    pass
#按照日期进行展示折线图
def getPlotDataByDate():
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime

    # 示例数据
    dates = ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']
    x_values = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
    y1_values = [10, 20, 15, 25, 18]
    y2_values = [5, 15, 10, 20, 12]

    # 生成日期折线图
    plt.plot_date(x_values, y1_values, label='线条1', linestyle='-', marker='o')
    plt.plot_date(x_values, y2_values, label='线条2', linestyle='-', marker='s')

    # 在每个数据点上方添加数字
    for date, y1, y2 in zip(x_values, y1_values, y2_values):
        plt.text(date, y1 + 1, str(y1), ha='center', va='bottom', color='blue')
        plt.text(date, y2 - 1, str(y2), ha='center', va='top', color='orange')

    # 添加标题和标签
    plt.title('时间折线图示例')
    plt.xlabel('日期')
    plt.ylabel('数值')

    # 格式化 x 轴日期
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    # 显示图例
    plt.legend()

    # 自动调整日期标签以避免重叠
    plt.gcf().autofmt_xdate()

    # 显示折线图
    plt.show()
#日或者周增长折线图
def getPlotByDayUP():
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime, timedelta

    # 示例数据（按日）
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 31)
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days+1 )]
    daily_values = [10, 20, 15, 25, 18, 22, 28, 30, 35, 40, 38, 45, 50, 48, 55, 60, 58, 65, 70, 68, 75, 80, 78, 85, 90, 88, 95, 100, 98, 105]

    # 计算日增长
    daily_growth = [daily_values[i] - daily_values[i - 1] if i > 0 else 0 for i in range(len(daily_values))]

    # 示例数据（按周）
    weekly_values = [sum(daily_growth[i:i + 7]) for i in range(0, len(daily_growth), 7)]
    weekly_dates = [date_range[i] for i in range(6, len(date_range), 7)]
    print(f'x_len={len(date_range)},y={len(daily_growth)}')
    print(f'x_len={len(weekly_dates)},y={len(weekly_values)}')
    # 生成折线图
    plt.plot_date(date_range[:-1], daily_growth, label='日增长', linestyle='-', marker='o', color='blue')
    plt.plot_date(weekly_dates, weekly_values[:-1], label='周增长', linestyle='-', marker='s', color='green')

    # 在每个数据点上方添加数字
    for date, growth in zip(date_range, daily_growth):
        plt.text(date, growth + 1, str(growth), ha='center', va='bottom', color='blue')

    for date, growth in zip(weekly_dates, weekly_values):
        plt.text(date, growth + 1, str(growth), ha='center', va='bottom', color='green')

    # 添加标题和标签
    plt.title('日增长与周增长折线图')
    plt.xlabel('日期')
    plt.ylabel('增长值')

    # 格式化 x 轴日期
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(r'%Y-%m-%d'))

    # 显示图例
    plt.legend()

    # 自动调整日期标签以避免重叠
    plt.gcf().autofmt_xdate()

    # 显示折线图
    plt.show()



if __name__=='__main__':
    #获取execl路径和新数据存储路径
    execl_dir=os.path.dirname(os.path.abspath(__file__))
    story_dir=os.path.dirname(os.path.abspath(__file__))
    #execl文件的匹配名
    fileNamePatter='111'
    #文件类型
    fileType='xlsx'
    #填补空白
    nanStr='空白'
    # 用于在图形中显示中文的设置
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文字体为黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题

    #获取execl
    fileList=getPatterFileList(execl_dir,fileNamePatter,fileType)
    #如果文件存在
    if fileList:
        #循环执行，获取所有文件信息
        for f in fileList:
            print(f'fileName={fileList}')
            #读取execl文件，并且填补空白
            new=getExeclDataNotNan(f,nanStr)
            print(f'dfData={new}')
            #按照模块名称分组获取数据
            groupData=getGroupDataByallValues(new,'模块')
            num_group_df=getNumByGroup(groupData)
            # title=f''
            print(f'对应模块数量\n{num_group_df}')
            #饼图展示
            # getPieData(num_group_df,'对应模块BUG数量分布')
            #用柱状图展示
            # getBarData(num_group_df,'对应模块BUG数量分布')
             #用折线图展示
            # getPlotData(num_group_df,'对应模块BUG数量分布')
            # getPlotDataByDate()
            getPlotByDayUP()

    else:
        print(f'not have {fileNamePatter}type 文件')






