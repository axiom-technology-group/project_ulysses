* 项目介绍

  用于提取和食物评论相关的短文本（80词左右）关键词

* 环境
  
  使用环境Python 3.6  <br>
  使用软件WING101， Pycharm也是可以的

* 使用方式
  
  安装Python 3.6 <br>
  安装jieba包 <br>
  安装Python WING IDE (WING的其他版本如101， Pycharm都是可以的) <br>
  将code文件中第三行  df = pd.read_csv('comment.csv', encoding='gb18030')  中comment.csv改为文件名称
  点击运行

* 期望效果 
  打印出按词性分类的词频统计，默认数量为10 <br>
  若需更改打印数量，可在第九行中    for (k,v) in c.most_common(10):  可将10改为任意值

  
