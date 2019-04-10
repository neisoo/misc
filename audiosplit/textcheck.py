# -*- coding: utf-8 -*-
#python3
from similarity.jarowinkler import JaroWinkler #https://github.com/luozhouyang/python-string-similarity
import logging
import sys
import os
import time
import json

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

# 模糊查找字符串
# 从srcText中查找dstText，相似度>0.9则认为找到。返回索引
def similarityFind(srcText, srcStart, dstText, maxWords = 30):
	jarowinkler = JaroWinkler()
	dstText = dstText.lower().strip()
	dstLen = len(dstText)
	lastword = dstText.split()[-1]
	maxSim = {'sim':0, 'begin':-1, 'end': -1}

	try:
		idx = srcStart
		count = 0;
		while count < maxWords:
			# 计算开始位置
			begin = idx
			while srcText[begin] == ' ':
				begin += 1

			end = begin + dstLen
			while srcText[end] != ' ':
				end += 1

			# 如果最后一个单词没有出现在查找范围中，适当的加大范围
			tempIdx = srcText[begin:end].lower().rfind(lastword)
			if tempIdx < 0:
				tempIdx = srcText[end: end + 15].lower().find(lastword)
				if tempIdx > 0:
					end += tempIdx + len(lastword)
					while srcText[end] != ' ':
						end += 1
			else:
				# 标点符号结尾
				tempIdx2 = srcText[begin:end].lower().rfind(', ')
				if tempIdx2 > tempIdx:
					end = begin + tempIdx2 + 1
				else:
					tempIdx2 = srcText[begin:end].lower().rfind('. ')
					if tempIdx2 > tempIdx:
						end = begin + tempIdx2 + 1
					else:
						tempIdx2 = srcText[begin:end].lower().rfind('! ')
						if tempIdx2 > tempIdx:
							end = begin + tempIdx2 + 1

			# 去掉标点符号
			temp = srcText[begin:end].lower()
			temp = temp.replace('"', '')
			temp = temp.replace('!', '')
			temp = temp.replace('?', '')
			temp = temp.replace('.', '')
			temp = temp.replace(',', '')
			temp = temp.replace('“', '')
			temp = temp.replace('”', '')
			temp = temp.replace('’', '')
			print('try:%s'%(temp))

			# 检查是否相似
			sim = jarowinkler.similarity(temp, dstText)
			print('sim:', sim)
			if sim > maxSim['sim']:
				#相似度开始下降时返回结果。
				maxSim['sim'] = sim
				maxSim['begin'] = begin
				maxSim['end'] = end
			else:
				srcWordList = srcText[maxSim['begin']:maxSim['end']].split()
				if len(srcWordList) > 0 and lastword != srcWordList[-1]:
					print('aaaaaaaaaaaaaaaa', srcWordList)
					print('bbbbbbbbbbbbbbbb', lastword)
					for i in range(len(srcWordList)-1,-1,-1):
						if srcWordList[i].find(lastword) >= 0:
							temp = ' '.join(srcWordList[0:i+1]).lower()
							temp = temp.replace('"', '')
							temp = temp.replace('!', '')
							temp = temp.replace('?', '')
							temp = temp.replace('.', '')
							temp = temp.replace(',', '')
							temp = temp.replace('“', '')
							temp = temp.replace('”', '')
							temp = temp.replace('’', '')
							print('ccccccccccccccccc1', temp)
							print('ccccccccccccccccc2', dstText)
							sim = jarowinkler.similarity(temp, dstText)
							print('ccccccccccccccccc3',sim)
							if sim > maxSim['sim']:
								maxSim['sim'] = sim
								maxSim['begin'] = begin
								end = srcText.rfind(lastword, begin, maxSim['end'])
								while srcText[end] != ' ':
									end += 1
								maxSim['end'] = end
								print('eeeeeeeeeeeeeeeeeeee', srcText[maxSim['begin']:maxSim['end']])
								break
				return maxSim

			# 继续从一下个单词开始比较。
			while srcText[begin] != ' ':
				begin += 1
			idx = begin
			count += 1
	except IndexError as e:
		print('error:', e)

	return maxSim

def textCheck(rootdir, txtdir):
	#用来判断文字相似度
	jarowinkler = JaroWinkler()

	for dirpath, dirs, files in os.walk(rootdir):            # 递归遍历当前目录和所有子目录的文件和目录
		#print(files)
		for name in files:                                   # files保存的是所有的文件名
			if os.path.splitext(name)[1] == '.json':
				filename = os.path.join(dirpath, name)       # 加上路径，dirpath是遍历时文件对应的路径
				textFileName = os.path.join(txtdir, os.path.split(dirpath)[1] + '.txt')
				checkSegment(filename, textFileName)

def checkSegment(filename, textFileName, segmentIdx=0, textIdx=0):
	#用来判断文字相似度
	jarowinkler = JaroWinkler()

	# 从json中读取分段信息。
	segment = []
	with open(filename, 'r', encoding='UTF-8') as f:
		segment = json.load(f)

		# 从txt中读取参考文字。
		with open(textFileName, 'r', encoding='UTF-8') as f:
			text = f.read()
			text = text.replace('\n', ' ')
			text = text.replace('\r', '')

			# 从指定位置开始校正。
			for i in range(segmentIdx, len(segment)):
				print('')
				print(i, textIdx)
				#print(text[textIdx:textIdx + 150])
				dstText = segment[i]['text'].lower().strip()
				print('audio say:[%s]'%dstText)
				
				ret = similarityFind(text, textIdx, dstText)
				print(ret)
				if ret['sim'] >= 0.8:
					print('[%s]%s'%(text[ret['begin']:ret['end']], text[ret['end']:ret['end']+150]))
					if not('texc' in segment[i].keys()):
						if not('textCheck' in segment[i].keys()):
							segment[i]['texc'] = text[ret['begin']:ret['end']].strip()
						else:
							segment[i]['texc'] = segment[i]['textCheck']
					if 'textCheck' in segment[i].keys():
						del segment[i]['textCheck']
					textIdx = ret['end']
				elif i+1 < len(segment):
					dstText = segment[i + 1]['text'].lower().strip()
					print('next audio say:[%s]****'%dstText)
					ret = similarityFind(text, textIdx, dstText)
					print(ret)
					if ret['sim'] >= 0.8:
						print('[%s]%s'%(text[textIdx:ret['begin']], text[ret['begin']:ret['begin']+150]))
						if not('texc' in segment[i].keys()):
							if not('textCheck' in segment[i].keys()):
								segment[i]['texc'] = text[textIdx:ret['begin']].strip()
							else:
								segment[i]['texc'] = segment[i]['textCheck']
								segment[i]['textCheck'] = null
						if 'textCheck' in segment[i].keys():
							del segment[i]['textCheck']
						textIdx = ret['begin']
					else:
						print(segment[i + 1]['text'].lower().strip())
						print(text[textIdx:textIdx+150])
						break;

	with open(filename, 'w', encoding='UTF-8') as f:
		json.dump(segment, f, indent = 4, sort_keys = True, ensure_ascii = False)
		print('--------------------------------')
	print('**********************************')
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

#mp3towav("./mp3", "./out/wav")
#audiosplit("./out/wav", "./out/split")
#audioReco("./out/split")
textCheck("./out/split", "./txt")

#s1='we tried to convince neil armstrong that he was really mrs roopy dressed in a spacesuit but'
#s2='we tried to convince neil armstrong that he was really mrs roopy dressed in a spacesuit'
#s3="we tried to convince niel armstrong that he was really misses ruby dressed in a space suit"
#jarowinkler = JaroWinkler()
#sim = jarowinkler.similarity(s1, s3)
#print(sim)
#sim = jarowinkler.similarity(s2, s3)
#print(sim)
