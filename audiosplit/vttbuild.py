# -*- coding: utf-8 -*-
#python3
from pydub import AudioSegment
import logging
import sys
import os
import time
import json
import re
import srt_tools.utils
import srt
from datetime import datetime,timedelta

#####################################################################
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

def validateTitle(title):
	rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
	new_title = re.sub(rstr, "_", title)  # 替换为下划线
	return new_title

def buildvttall(rootdir, mp3dir, outputDir):
	for dirpath, dirs, files in os.walk(rootdir):            # 递归遍历当前目录和所有子目录的文件和目录
		print(files)
		for name in files:                                   # files保存的是所有的文件名
			if os.path.splitext(name)[1] == '.json':
				filename = os.path.join(dirpath, name)       # 加上路径，dirpath是遍历时文件对应的路径
				mp3FileName = os.path.join(mp3dir, os.path.splitext(name)[0] + '.mp3')
				buildmp3(filename, mp3FileName, outputDir)
				buildvtt(filename, outputDir)

def buildmp3(filename, mp3FileName, outputDir):
	sound = AudioSegment.from_file(mp3FileName, "mp3")

	# 从json中读取分段信息。
	info = {}
	with open(filename, 'r', encoding='UTF-8') as f:
		info = json.load(f)
		print(info['chapter'])
		for chapter in info['chapter']:
			# 分割音频文件
			splitStart = info['split'][chapter['start']]
			splitEnd = info['split'][chapter['end']]
			chunk = sound[splitStart['start']:splitEnd['end']]
			chunk.export('%s/%s.ogg'%(outputDir, validateTitle('%02d_%s_%02d_%s'%(info['book']['index'] + 1, info['book']['name'], chapter['index'], chapter['title']))), format="ogg")
	return

def buildvtt(filename, outputDir):
	# 从json中读取分段信息。
	info = {}
	with open(filename, 'r', encoding='UTF-8') as f:
		info = json.load(f)
		print(info['chapter'])
		for chapter in info['chapter']:
			subs = []
			index = 0
			offset = info['split'][chapter['start']]['start']
			for i in range(chapter['start'], chapter['end'] + 1):
				split = info['split'][i]
				start = timedelta(milliseconds=(split['start'] - offset))
				end = timedelta(milliseconds=(split['end'] - offset))
				content = split['textCheck']
				subs.append(srt.Subtitle(index, start, end, content))
				index += 1

			# 保存vtt字幕文件
			vttfilename = '%s/%s.vtt'%(outputDir, validateTitle('%02d_%s_%02d_%s'%(info['book']['index'] + 1, info['book']['name'], chapter['index'], chapter['title'])))
			with open(vttfilename, 'w') as f:
				print(subs)
				f.write(srt.compose(subs))
	return

mkdir(outputPath)
mkdir("./out/mp3")

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

buildvttall("./vtt", "./mp3", "./out/mp3")
