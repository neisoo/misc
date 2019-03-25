# -*- coding: utf-8 -*-
#python3
import glob
import os.path
import logging
import re
import json

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


#从指定目录下的文本文件中找取所有不在old_word_dict中的单词，并统计出现次数
def get_new_word_list(file_path, old_word_dict):
    file_list = os.listdir(file_path) #文件列表
    word_dict = {}
    word_list = []
    word_re = re.compile(r'[\w]+') #字符串前面加上r表示原生字符串，\w 匹配任何字类字符，包括下划线。与“[A-Za-z0-9_]”等效
    for file_name in file_list:
        if os.path.isfile(file_name) and os.path.splitext(file_name)[1] == '.txt': #os.path.splitext('c:\\csv\\test.csv') 结果('c:\\csv\\test', '.csv')
            try:
                f = open(file_name,'r', encoding='UTF-8')
                data = f.read()
                f.close()
                words = word_re.findall(data)#findall()返回的是括号所匹配到的结果（如regex1），多个括号就会返回多个括号分别匹配到的结果（如regex），如果没有括号就返回就返回整条语句所匹配到的结果(如regex2)
                for word in words:
                    if word.isdigit(): #全是数字，跳过。
                        continue;
                    if len(word) <= 1: #字母，跳过。
                        continue;
                    word = word.lower()
                    if word in old_word_dict: #在单词表中已经有，跳过。
                        continue;
                    if word not in word_dict:
                        word_dict[word] = 1 #从1为索引保存单词
                        word_list.append(word)
                    else:
                        word_dict[word] += 1
            except:
                print('open %s Error' % file_name)

    result_list = sorted(word_dict.items(), key=lambda t :t[1], reverse = True) #t[0]按key排序，t[1]按value排序？ 取前面系列中的第二个参数做排序
    for key, value in result_list:
        logger.info('%5d\t%s' % (value, key))
    print('count:%d' % (len(result_list)))
    return word_list

#从英语__麦克米伦高频词汇.json词典中找出已有的单词。
def get_old_word_list():
    old_word_dict = {}

    load_f = open("../记忆库/英语__麦克米伦高频词汇/英语__麦克米伦高频词汇.json", 'r', encoding='UTF-8')
    load_dict = json.load(load_f)
    for note in load_dict["notes"]:
        if note['fields'][0] not in old_word_dict:
            old_word_dict[note['fields'][0]] = 1
        else:
            old_word_dict[note['fields'][0]] += 1
    print(old_word_dict)
    return old_word_dict

mkdir(outputPath)
old_word_dict = get_old_word_list()
new_word_list = get_new_word_list('.', old_word_dict)

#生成单词列表，这些单词出现在当前目录的txt中，便不在alread_have.json字典中。
with open('.\\out\\wordlist.json', 'w') as f:
    json.dump(new_word_list, f, indent = 4, sort_keys = True)
