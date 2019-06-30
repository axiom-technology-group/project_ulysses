
import requests
import json
import re
import csv
import time


class collegeSpider():
 
    def __init__(self):
        # 创建
        with open('test.csv', 'a',encoding='utf-8-sig') as csvfile:
            fieldnames = ['排名', '学校名称', '类型', '所在地', '提供学位', '毕业五年后月薪']
            self.writer = csv.writer(csvfile)
            self.writer.writerow(fieldnames)
        # 请求
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        }
        self.page = 1

    def getData(self, page):
        print('正在爬取%d页' % page)
        # 发起请求
        response = requests.get(
            'https://www.wmzy.com/api/rank/school?diploma_id=7&sort_by=xinchou&province_id=&sch_type_name=&sch_rank_type=&search_key=&page={0}&page_len=20&_=1561717610023'.format(
                page),
            headers=self.headers)
        # 转字典
        content = json.loads(response.text)
        # 解析
        self.parse(content['htmlStr'])
        # 下一页？
        hasmore = content['hasMore']
        # 下一页 = 1
        if hasmore:
            time.sleep(1)
            self.page += 1
            self.getData(self.page)

    def parse(self, content):
        # 解析json
        pattern = re.compile(
            r'<td\sclass="col1td">.*?>(.*?)</span>.*?<td.*?<a.*?>(.*?)</a>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td.*?>(.*?)</td>',
            re.S)

        colleges = pattern.findall(content)

        # 写入
        for college_info in colleges:
            with open('test.csv', 'a',encoding='utf-8-sig') as csvfile:
                self.writer = csv.writer(csvfile)
                self.writer.writerow(college_info)


if __name__ == '__main__':
    cs = collegeSpider()
    cs.getData(cs.page)
