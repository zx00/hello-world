import os 
import re

print('hello world')


txt="""Python3 高级开发工程师 上海互教教育科技有限公司上海-浦东新区2万/月02-18满员
测试开发工程师（C++/python） 上海墨鹍数码科技有限公司上海-浦东新区2.5万/每月02-18未满员
Python3 开发工程师 上海德拓信息技术股份有限公司上海-徐汇区1.3万/每月02-18剩余11人
测试开发工程师（Python） 赫里普（上海）信息科技有限公司上海-浦东新区1.1万/每月02-18剩余5人
Python高级开发工程师 上海行动教育科技股份有限公司上海-闵行区2.8万/月02-18剩余255人
python开发工程师 上海优似腾软件开发有限公司上海-浦东新区2.5万/每月02-18满员"""

re=re.compile(r'(?P<mounth>[1-9])+万/(.*?)月')

list=re.findall(txt)

print(f'a={list}')

for i in re.finditer(txt):
    print(f'i={i.group("mounth")}')
    
for j in list:
    print(f'a={j[0]}')