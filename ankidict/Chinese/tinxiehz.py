# -*- coding: utf-8 -*-
#python3
import glob
import os.path
import logging
import re
from bs4 import BeautifulSoup
import json
import requests 
import uuid
import string

import pyaudio
import wave

import time
import hashlib
from urllib import parse

outputPath = "./out"

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

#从百度汉语获取汉字的拼音和组词
def HZdict(word=None):
	result = {}
	headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'} #伪装成google浏览器,因为服务器根据 UA 来判断拒绝了 python 爬虫。

	#url = 'http://dict.youdao.com/search?q=%s' % (word)
	url = 'https://hanyu.baidu.com/s?wd=%s&ptype=zici' % (word)
	#print("bbb111:%s,url=%s"%(word, url))
	response = requests.post(url, headers=headers, timeout=5)
	response.encoding = 'utf-8'
	#print("bbb222")
	soup = BeautifulSoup(response.text, "html.parser")
	pinyinDiv = soup.find(attrs={"id":"pinyin"})
	#print("bbb333")
	result['Pinyin'] = []
	if not pinyinDiv is None:
		pinyins = pinyinDiv.find_all('b')
		if len(pinyins) > 0:
			result['Pinyin'].append(str(pinyins[0].string).replace('[', '').replace(']', '').strip())

		if len(pinyins) > 1:
			result['Pinyin'].append(str(pinyins[1].string).replace('[', '').replace(']', '').strip())

	result['Zuci'] = []
	zuciDiv = soup.find(attrs={"id":"zuci-wrapper"})
	if not zuciDiv is None:
		#print("bbb444")
		zucis = zuciDiv.find_all('a')
		if len(zucis) > 0:
			result['Zuci'].append(str(zucis[0].string).strip())
		#if len(zucis) > 1:
		#	result['Zuci'].append(str(zucis[1].string).strip())
		#if len(zucis) > 2:
		#	result['Zuci'].append(str(zucis[2].string).strip())

	#print("bbb555")
	#print(result)
	return result

def ankijson(srcData, dstData):
	MAX_TRY_COUNT = 10
	wordlist = srcData['wordlist']
	
	for i in range(0, len(wordlist)):
	#for i in range(0, 3):

		words = wordlist[i]['words']
		lesson = wordlist[i]['lesson']

		for keyword in words:
			tryCount = 0
			while tryCount < MAX_TRY_COUNT:
				try:
					#print("[%d]=%s=====================" % (i, keyword))
					word = HZdict(keyword)
					#print("aaa111")
					"""
					"__type__": "Note",
					"data": "",
					"fields": [
						"课文1",
						"诗",
						"shī",
						"",
						"诗，诗歌"
					],
					"flags": 0,
					"guid": "3d54c940-32bd-11e9-be88-ac9e17867d04",
					"note_model_uuid": "86949c90-2f59-11e9-82b0-180373427d86",
					"tags": []
					"""
					
					anki = {}
					anki['__type__'] = "Note"
					anki['data'] = ""
					anki['flags'] = 0
					anki['note_model_uuid'] = "86949c90-2f59-11e9-82b0-180373427d86" #要改成正确值
					anki['tags'] = []
					anki['guid'] = str(uuid.uuid1())#str(uuid.uuid1())[0:8]

					anki['fields'] = []
					anki['fields'].append(lesson)
					anki['fields'].append(keyword)

					anki['fields'].append(word['Pinyin'][0])
					#print("aaa222")

					if len(word['Pinyin']) > 1:
						anki['fields'].append(word['Pinyin'][1])
					else:
						anki['fields'].append('')

					anki['fields'].append("%s，%s" % (keyword, '，'.join(word['Zuci'])))
					#print("aaa333")

					break

				except AttributeError as err:
					print(err)
					print("****try count %d" % (tryCount))
					tryCount = tryCount + 1
					time.sleep(2)
				except ConnectionResetError as err:
					print(err)
					print("$$$$try count %d" % (tryCount))
					tryCount = tryCount + 1
					time.sleep(10)
				except KeyError as err:
					print(err)
					print("$$$$try count %d" % (tryCount))
					tryCount = tryCount + 1
				except requests.exceptions.ConnectionError as err:
					print(err)
					print("++++try count %d" % (tryCount))
					tryCount = tryCount + 1
					time.sleep(10)
				except requests.exceptions.ReadTimeout as err:
					print(err)
					print("----try count %d" % (tryCount))
					tryCount = tryCount + 1
					time.sleep(10)

			if tryCount >= MAX_TRY_COUNT:
				data = {}
				data['lesson'] = lesson
				data['word'] = keyword
				errorData.append(data)

				anki = {}
				anki['__type__'] = "Note"
				anki['data'] = ""
				anki['flags'] = 0
				anki['note_model_uuid'] = "86949c90-2f59-11e9-82b0-180373427d86" #要改成正确值
				anki['tags'] = []
				anki['guid'] = str(uuid.uuid1())#str(uuid.uuid1())[0:8]

				anki['fields'] = []
				anki['fields'].append(lesson)
				anki['fields'].append(keyword)
				anki['fields'].append('') #Pinyin
				anki['fields'].append('') #Pinyin2
				anki['fields'].append('') #Zuci

			dstData.append(anki)

			logger.info("%s," % (json.dumps(anki, ensure_ascii=False, indent=4)))
			#print(anki['fields'])
			#print("=========================")
	#print(dstData)
	return

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

srcData = {}
dstData = []
errorData = []

# Reading data
with open('.\\tinxiehz.json', 'r', encoding='UTF-8') as f:
	srcData = json.load(f)

ankijson(srcData, dstData)
logger.info("\n\n ================ Totals: %d records ===============" % (len(dstData)))
with open('.\\out\\output.json', 'w') as f:
	json.dump(dstData, f, indent = 4, sort_keys = True, ensure_ascii = False)

with open('.\\out\\error.json', 'w') as f:
	json.dump(errorData, f, indent = 4, sort_keys = True, ensure_ascii = False)