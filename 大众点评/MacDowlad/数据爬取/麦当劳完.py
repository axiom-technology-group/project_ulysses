import time
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import pandas as pd
import os

def login():
    #登录
    loginButton = driver.find_elements_by_css_selector('#top-nav > div > div.group.quick-menu > span.login-container.J-login-container > a:nth-child(1)')
    loginButton[0].click()


def pageBottom(browser): 
    #滚动条移动至页面底部 ajax
    js = "var q=document.documentElement.scrollTop=100000"
    browser.execute_script(js)

option = ChromeOptions()
#启动开发者模式  属性正常
option.add_experimental_option('excludeSwitches', ['enable-automation'])

# 不加载图片, 提升速度
option.add_argument('blink-settings=imagesEnabled=false') 

driver = Chrome(options=option)
url = "https://www.dianping.com/"
driver.get(url)
login()
#等待登录
loginFlag = input()

url_maidanglao = 'http://www.dianping.com/search/keyword/2/10_%E9%BA%A6%E5%BD%93%E5%8A%B3/r14'
driver.get(url_maidanglao)
#解析器（特殊情况需更换） driver.page_source == 获取网页源码 url=dirver.page...
soup = BeautifulSoup(driver.page_source,'lxml')
#找到该页面下所有商品
allLink = soup.select('div.shop-list.J_shop-list.shop-all-list ul li')
bianhao = []
page_ = 1
try:
    while(page_<6):
        print("page:{}".format(page_))
        # 拿到所有商品链接
        for l in allLink:
            bianhao.append(l.select('div.pic a')[0].get('href'))#拿去单个商品
            #下一页
            driver.find_element_by_css_selector('a.next').click()
            soup = BeautifulSoup(driver.page_source, 'lxml')
            allLink = soup.select('div.shop-list.J_shop-list.shop-all-list ul li')
            page_ = page_+1
except Exception:
    pass
    
#分割网站取编号
bianhao = [int(i.split('/')[-1]) for i in bianhao]
#保险
bianhao = list(set(bianhao))

page = 0
num = 0
#创建二维数组做库
df = pd.DataFrame({'name': [], 'address':[],'commentNum':[],'price':[],'kouwei':[],"huanjing":[],"fuwu":[],\
                   "goodComment":[],'midComment':[],'badComment':[]})

while(num<len(bianhao)):
    try:
        dianpuhao = bianhao[num]
        num = num +1
        url = "https://www.dianping.com/shop/"+str(dianpuhao)+"/review_all"
        driver.get(url)
        pageBottom(driver)
        #提取店铺名
        name = driver.find_element_by_css_selector("h1.shop-name").text
        print("金拱门:{}".format(name))
        page = 1
        #提取评论数量
        commentNum = driver.find_element_by_css_selector('span.reviews').text
        #提取人均价格
        price = driver.find_element_by_css_selector("span.price").text
        #提取口味 环境 服务
        scores = [i.text for i in driver.find_elements_by_css_selector("div.rank-info span.score span")]
        #提取地址
        address = driver.find_element_by_css_selector('div.address-info').text
        #提取好评数量
        try:
            goodComment = driver.find_element_by_css_selector("div.filters label.filter-item.filter-good span.count").text.replace("(",'').replace(")",'')
        except Exception:
            goodComment = "好评:0"
        #提取中评数量
        try:
            midComment = driver.find_element_by_css_selector("div.filters label.filter-item.filter-middle span.count").text.replace("(",'').replace(")",'')
        except Exception:
            midComment = '中评:0'
        #提取差评数量
        try:
            badComment = driver.find_element_by_css_selector("div.filters label.filter-item.filter-bad span.count").text.replace("(",'').replace(")",'')
        except Exception:
            badComment = '差评:0'
        #入库
        df = df.append(pd.DataFrame({'name': [name], 'address':[address],'commentNum':[commentNum],'price':[price],'kouwei':[scores[0]],"huanjing":[scores[1]],"fuwu":[scores[2]],\
                       "goodComment":[goodComment],'midComment':[midComment],'badComment':[badComment]}))
        #去除重复内容
        df.drop_duplicates(inplace=True)
        #写入csv文件
        df.to_csv("朝阳区-麦当劳.csv",index=False,encoding="utf_8_sig")
        # df = pd.DataFrame({'name': [], 'date': [], 'comment': []})
        # df = pd.DataFrame({'name': [], 'date': [], 'comment': [],'related-comment':[]})
        # showAll = driver.find_elements_by_css_selector('div.info.J-info-short.clearfix a')
        
        #加载更多评论，会跳出新的页面
        showAll = driver.find_elements_by_css_selector("div.more-words a")
        try:
            for i in showAll:
                i.click()
        except Exception:
            pass

        soup = BeautifulSoup(driver.page_source)
        #提取评论文本
        text = [i.text.replace("\n",'').replace(" ",'').replace('收起评论','')+'\r\n' for i in soup.select('div.review-words')]##似乎有问题，没处理有Img标签的内容 如西大望店
        # 评论写入txt文件
        with open("{name}.txt".format(name=name),'a',encoding='utf-8') as f:
            f.writelines(text)
        #评论翻页
        while(True):
            try:
                driver.find_element_by_css_selector('a.NextPage').click()
            except Exception:
                break
            page=page+1
            print("page:{}".format(page))
            pageBottom(driver)
            showAll = driver.find_elements_by_css_selector("div.more-words a")
            try:
                for i in showAll:
                    i.click()
            except Exception:
                pass
            soup = BeautifulSoup(driver.page_source)
            text = [i.text.replace("\n", '').replace(" ", '').replace('收起评论', '') + '\r\n' for i in
                    soup.select('div.review-words')]
            with open("{name}.txt".format(name=name), 'a', encoding='utf-8') as f:
                f.writelines(text)
    except Exception: 
        print("遇到验证码{}".format(page))
        input("验证码")
        os.remove('{name}.txt'.format(name=name))
        num = num-1
