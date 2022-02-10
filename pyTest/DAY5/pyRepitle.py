import urllib.request
import urllib3
from bs4 import BeautifulSoup
# url="https://www.baidu.com/"
url="https://www.douban.com/"
# print(dir(urllib))
# print(help(urllib))
respon = urllib.request.urlopen(url)
# print(respon)
# print(respon.read())
#下载器
def urlDownload(url) :
    #urlib.request创建请求，打开URL
    respon = urllib.request.urlopen(url)
    responContent=respon.read()
    responCode=respon.getcode()
    return responContent,responCode
#网页下载内容本地保存
def loadDownload(file,content) :
    #以二进制打开文件写入
    f=open(file,"wb")
    f.write(content)
    f.close


#网页解析器
def urlParser(html) :
    # pass
#创建beautifulsoupj解析对象
 soup= BeautifulSoup(html,"html.parser",from_encoding="utf-8")
 #获取所有content
#  content=soup.find_all('noscript')[0].content
 print("content内容",content)

 #获取所有

responContent,responCode=urlDownload(url)
print("类型",type(responContent))
print("url网页内容\n",responContent)
print("url访问结果",responCode)
loadDownload("test1.html",responContent)
urlParser('test1.html')
# print(bs4)