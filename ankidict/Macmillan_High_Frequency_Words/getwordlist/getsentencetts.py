# -*- coding: utf-8 -*-
#python3
import glob
import os.path
import logging
import re
import json
import copy
import requests
import time

outputPath = "./out"
audioPath = "./out/audio"
        
def mkdir(path):
	# 去除首位空格
	path=path.strip()
	# 去除尾部 \ 符号
	path=path.rstrip("\\")

	# 判断路径是否存在
	# 存在     True
	# 不存在   False
	isExists=os.path.exists(path)

	# 判断结果
	if not isExists:
		# 如果不存在则创建目录
		# 创建目录操作函数
		os.makedirs(path) 

		return True
	else:
		# 如果目录存在则不创建，并提示目录已存在
		return False

mkdir(outputPath)

logger = logging.getLogger("mylog")
logger.setLevel(logging.DEBUG)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler(".\\out\\logging.log", encoding="utf-8")
fh.setLevel(logging.DEBUG)
# 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# 设置日志格式
#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
formatter = logging.Formatter("%(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
#将相应的handler添加在logger对象中
logger.addHandler(ch)
logger.addHandler(fh)


#从英语__麦克米伦高频词汇.json词典中找出例句，并下载例句的tts语音文件。
def gettts():
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'} #伪装成google浏览器,因为服务器根据 UA 来判断拒绝了 python 爬虫。
    load_f = open("../记忆库/英语__麦克米伦高频词汇/英语__麦克米伦高频词汇.json", 'r', encoding='UTF-8')
    load_dict = json.load(load_f)

    for i in range(0, len(load_dict["notes"])):
        note = load_dict["notes"][i]
        if len(note['fields'][8]) > 0:
            #下载单词发音文件
            print("%d-%s-%s" % (i, note['fields'][0], note['fields'][8]))

            #url = "https://fanyi.baidu.com/gettts?lan=en&text=%s&spd=3&source=web" % note['fields'][8]
            #r = requests.get(url, headers=headers, timeout=10) #例句tts
            #with open("./out/audio/normal/%s_3.mp3" % (note['fields'][0]), "wb") as ttsfile:
            #    ttsfile.write(r.content)
            #time.sleep(1)

            url = "https://fanyi.baidu.com/gettts?lan=en&text=%s&spd=1&source=web" % note['fields'][8]
            r = requests.get(url, headers=headers, timeout=10) #例句tts
            with open("./out/audio/slow/%s_3.mp3" % (note['fields'][0]), "wb") as ttsfile:
                ttsfile.write(r.content)
            time.sleep(1)


    return

mkdir(outputPath)
mkdir("./out/audio/normal")
mkdir("./out/audio/slow")

word_dict = gettts()
