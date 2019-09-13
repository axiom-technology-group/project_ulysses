

'''
爬取APP store的 免费和付费榜单
https://www.apple.com/cn/itunes/charts/free-apps/

软件名称、供应商、大小、类别、兼容性、语言、年龄分级、Copyright、价格、评分、评分数量
'''

import csv
import requests
import time
from lxml import etree
import re


class APPSpider:
    def __init__(self):
        # 列表页的地址，通过列表页地址得到详情页的url。
        self.mainUrlList = ["https://www.apple.com/cn/itunes/charts/free-apps/",
                            "https://www.apple.com/cn/itunes/charts/paid-apps/", ]

        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        }

        self.file_name = "App.csv"

    def get_response_xpath(self, url):
        """发送请求获取可xpath的响应对象"""
        response = requests.get(url, headers=self.headers)
        response = response.content.decode()
        return etree.HTML(response)

    def save_item_in_csv(self, item, titleNum):
        """保存数据item到csv里面，方式a"""
        with open(self.file_name, "a", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=item.keys())
            if titleNum == 0:
                writer.writeheader()
            writer.writerow(item)

    def get_info(self, item, li):
        """提取数据"""

        item["url"] = li.xpath("./a/@href")
        item["url"] = item["url"][0] if len(item["url"]) > 0 else None

        # 发送详情页链接，获取详情页数据
        response = self.get_response_xpath(item["url"])
        item["name"] = response.xpath(
            "//header[@class='product-header app-header product-header--padded-start']/h1/text()")
        item["name"] = item["name"][0].strip() if len(item["name"]) > 0 else None
        item["desc"] = response.xpath(
            "//header[@class='product-header app-header product-header--padded-start']/h2/text()")
        item["desc"] = item["desc"][0].strip() if len(item["desc"]) > 0 else None

        item["company"] = response.xpath(
            "//header[@class='product-header app-header product-header--padded-start']/h2[@class='product-header__identity app-header__identity']/a/text()")
        item["company"] = item["company"][0].strip() if len(item["company"]) > 0 else None

        item["company_EnglishName"] = response.xpath("//dt[text()='供应商']/../dd/text()")
        item["company_EnglishName"] = item["company_EnglishName"][0].strip() if len(
            item["company_EnglishName"]) > 0 else None

        item["size"] = response.xpath("//dt[text()='大小']/../dd/text()")
        item["size"] = item["size"][0].strip() if len(item["size"]) > 0 else None

        item["type"] = response.xpath(
            "//dl[@class='information-list information-list--app medium-columns']/div[3]/dd/a/text()")
        item["type"] = item["type"][0].strip() if len(item["type"]) > 0 else None

        item["compatibility"] = response.xpath("//dt[text()='兼容性']/..//p/text()")
        item["compatibility"] = item["compatibility"][0].strip() if len(item["compatibility"]) > 0 else None

        item["language"] = response.xpath("//dt[text()='语言']/..//p/text()")
        item["language"] = item["language"][0].strip() if len(item["language"]) > 0 else None

        item["age"] = response.xpath("//dt[text()='年龄分级']/../dd/text()")
        item["age"] = item["age"][0].strip() if len(item["age"]) > 0 else None

        item["Copyright"] = response.xpath("//dt[text()='Copyright']/../dd/text()")
        item["Copyright"] = item["Copyright"][0].strip() if len(item["Copyright"]) > 0 else None

        item["rank"] = response.xpath(
            "//header[@class='product-header app-header product-header--padded-start']/ul[@class='product-header__list app-header__list']//li[@class='inline-list__item']/text()")
        item["rank"] = item["rank"][0].strip() if len(item["rank"]) > 0 else None

        try:
            pingfen = response.xpath("//figcaption[@class='we-rating-count star-rating__count']/text()")[0].strip()
            item["star"] = re.findall(r'(.*?)，.*评分', pingfen)[0]
            item["commentCount"] = re.findall(r'.*，(.*?) 个评分', pingfen)[0].strip()
        except:
            item["star"] = None
            item["commentCount"] = None

        item["priceType"] = response.xpath(
            "//li[@class='inline-list__item inline-list__item--bulleted app-header__list__item--price']/text()")
        item["priceType"] = item["priceType"][0] if len(item["priceType"]) > 0 else None

        return item

    def run(self):
        # 创建表头
        titleNum = 0

        # 免费和付费的都要爬取
        for url in self.mainUrlList:

            # 发送列表页请求
            response = self.get_response_xpath(url)
            li_list = response.xpath("//section[@class='section apps grid']/ul/li")
            print(len(li_list))  # 100个
            for li in li_list:
                item = {}
                # 提取100个APP的数据
                self.get_info(item, li)

                # 保存数据
                print(item)
                self.save_item_in_csv(item, titleNum)
                titleNum = 999


if __name__ == '__main__':
    appspider = APPSpider()
    appspider.run()
