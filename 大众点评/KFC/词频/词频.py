import jieba
import pandas as pd
txt = open("santi.txt", encoding="utf-8").read()
words  = jieba.lcut(txt)
counts = {}
for word in words:
    counts[word] = counts.get(word,0) + 1
items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True)
for i in range(30): #打印前30名
    word, count = items[i]
    print ("{0:<10}{1:>5}".format(word, count))

print ("--------------------------------------")


import jieba
txt = open("santi.txt", encoding="utf-8").read()
#加载停用词表
stopwords = [line.strip() for line in open("CS.txt",encoding="utf-8").readlines()]
words  = jieba.lcut(txt)
counts = {}
for word in words:
    #不在停用词表中
    if word not in stopwords:
        #不统计字数为一的词
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word,0) + 1
items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True)
for i in range(30):
    word, count = items[i]
    print ("{:<10}{:>7}".format(word, count))


txt.to_csv('Result1.csv',encoding='utf-8')
