import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://baike.baidu.com/item/%E4%BA%BA%E6%B0%91%E7%9A%84%E5%90%8D%E4%B9%89/17545218"


response = urllib.request.urlopen(url)
con = response.read()
#使用beautifulsoup中的html解析器
cont = BeautifulSoup(con,"html.parser") #beautifulsoup是一个解析器，可以特定的解析出内容
content = cont.find_all('ul', {'id':'dramaSerialList'})
content = str(content)
##去掉HTML标签
content1 = re.sub(r'<[^>]+>', '', content)
f = open('drama.txt', 'w', encoding='utf-8') #直接用open打开会报错，需要指定编码方式
f.write(content1)
f.close()
# changes
