# -*- coding: utf-8 -*-
#python3
import glob
import os.path
import logging
import re
import json
import copy

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


#从英语__麦克米伦高频词汇.json词典中找出不重复的笔记的单词。
def remove_duplicate_word():
    word_dict = {}
    duplicate_word_list = []

    load_f = open("../记忆库/英语__麦克米伦高频词汇/英语__麦克米伦高频词汇.json", 'r', encoding='UTF-8')
    load_dict = json.load(load_f)
    new_dict = copy.deepcopy(load_dict)
    new_dict["notes"] = [];

    for note in load_dict["notes"]:
        if note['fields'][0] not in word_dict:
            word_dict[note['fields'][0]] = 1
            new_dict["notes"].append(note);
        else:
            print(note['fields'][0])
            duplicate_word_list.append(note['fields'][0]);

    print("count:%d" % (len(duplicate_word_list)))
    return new_dict

mkdir(outputPath)
word_dict = remove_duplicate_word()
word_dict["notes"] = sorted(word_dict["notes"],key=lambda x:str.lower(x['fields'][0]))

#生成单词列表，这些单词出现在当前目录的txt中，便不在alread_have.json字典中。
with open('.\\out\\dict.json', 'w', encoding='utf-8') as f:
    json.dump(word_dict, f, indent = 4, sort_keys = True, ensure_ascii = False)
