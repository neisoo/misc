# -*- coding: utf-8 -*-
#python3
import glob
import os.path
import logging
import re
import json
import uuid
import string
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


def buildDicJson(inputFileName, outputFileName):
	# 从json中读取分段信息。
	info = {}
	notes = []
	with open(inputFileName, 'r', encoding='UTF-8') as f:
		info = json.load(f)
		for item in info['itemlist']:
			"""
			{
				"__type__": "Note",
				"data": "",
				"fields": [
					"和倍问题01",
					"果园里有桃树和梨树共150棵，桃树比梨树多40棵，两种果树各多少棵？",
					"01_01_01",
					"01_01_01"
				],
				"flags": 0,
				"guid": "f<p9d(3=_)",
				"note_model_uuid": "14f4fb52-5eb3-11e9-af5c-ac9e17867d04",
				"tags": []
			}
			"""
			
			anki = {}
			anki['__type__'] = "Note"
			anki['data'] = ""
			anki['flags'] = 0
			anki['note_model_uuid'] = "14f4fb52-5eb3-11e9-af5c-ac9e17867d04" #要改成正确值
			anki['tags'] = []
			anki['guid'] = str(uuid.uuid1())#str(uuid.uuid1())[0:8]

			anki['fields'] = []
			anki['fields'].append(item['tx'])
			anki['fields'].append(item['ti'])
			anki['fields'].append(item['daid'])
			anki['fields'].append(item['jjid'])

			notes.append(anki)

	# 保存输出文件
	with open(outputFileName, 'w', encoding='UTF-8') as f:
		json.dump(notes, f, indent = 4, sort_keys = True, ensure_ascii = False)
		print('done.')

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

buildDicJson('./tssx_cj.json', './out/tssx_cj_notes.json')
