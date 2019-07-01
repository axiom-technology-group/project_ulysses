## CollegeSpider.py 是一个用于爬取项目， 用于爬取https://www.wmzy.com/api/rank/schList 中大学的毕业薪酬

* 环境
  
使用环境Python 3.6
使用软件WING101， Pycharm也是可以的

* 使用方式

安装Python 3.6
安装Python WING IDE (WING的其他版本如101， Pycharm都是可以的)
双击CollegeSpider.py后保存当前文件到指定路径，点击上方运行按钮即可

* 期望效果 

当程序运行中
右下角会不断出现"正在爬取第X页"
当程序爬取完所有资料
右下角会出现"over"
在指定目录下同时会新建一个名为"test.csv"的csv文件

* 爬取其他同类网站方式 

当发现网站内容有变动需要后期维护时，更改代码中的 #解析json部分（具体的根据网站源代码修改）
当发现爬虫被拒时，更改代码中 #请求部分（网上搜一个IP即可）
除了 #解析json #请求  两部分，其余代码大部分不需要改动
