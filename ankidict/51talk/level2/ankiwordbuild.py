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

def ankijson(bookList, ankiList):
	for i in range(0, len(bookList)):
		bookListItem = bookList[i]
		logger.info("\n\n=== Process %s ===" % bookListItem['params'])

		print(bookListItem['word_ref'])
		word_ref = bookListItem['word_ref']
		source = "%s_%s_%s"%(bookListItem['level_str'], bookListItem['unit_str'], bookListItem['lesson_str'])
		for j in range(0, len(word_ref)):
			#"__type__": "Note", 
			#"data": "", 
			#"fields": [
			#	"thirteen", 
			#	"[sound:0a0f038f0844a6732c61e49e6df8d6f4_1611153c4.mp3]", 
			#	"<div>There are <font color=\"#ff0000\">thirteen</font> apples.[sound:ac34af028f53e9cb0cd1e99ba0d501e7_16111527b.mp3]</div><div><br /></div><div>I am <font color=\"#ff0000\">thirteen</font> years old.[sound:497139987e5f406aa003522aee97a3bf_161115b83.mp3]</div>"
			#], 
			#"flags": 0, 
			#"guid": "g+/XyaNq5h", 
			#"note_model_uuid": "e21b0d8f-b1b9-11e8-a35c-180373427d85", 
			#"tags": []
			anki = {}
			anki['__type__'] = "Note"
			anki['data'] = ""
			anki['flags'] = 0
			anki['note_model_uuid'] = "e21b0d8f-b1b9-11e8-a35c-180373427d85"
			anki['tags'] = []
			anki['guid'] = str(uuid.uuid1())[0:8]

			title = word_ref[j]['title']
			url = word_ref[j]['url']
			sentence1 = word_ref[j]['sentence1']
			sentence1_url = word_ref[j]['sentence1_url']
			sentence2 = word_ref[j]['sentence2']
			sentence2_url = word_ref[j]['sentence2_url']

			sentence = ""
			if sentence1:
				sentence += "<div>"
				sentence1 = sentence1.split()
				for k in range(0, len(sentence1)):
					str1 = sentence1[k].lower().strip()
					table=str.maketrans('','',string.punctuation)
					str1 = str1.translate(table)
					str2 = title.lower().strip()
					if str1 == str2:
						sentence += "<font color=\"#ff0000\">" + sentence1[k] + "</font> "
					else:
						sentence += sentence1[k] + " "
				sentence += "[sound:%s]</div>" % (sentence1_url)

			if sentence2:
				sentence += "<br /><div>"
				sentence2 = sentence2.split()
				for k in range(0, len(sentence2)):
					str1 = sentence2[k].lower().strip()
					table=str.maketrans('','',string.punctuation)
					str1 = str1.translate(table)
					str2 = title.lower().strip()
					if str1 == str2:
						sentence += "<font color=\"#ff0000\">" + sentence2[k] + "</font> "
					else:
						sentence += sentence2[k] + " "
				sentence += "[sound:%s]</div>" % (sentence2_url)

			anki['fields'] = []
			anki['fields'].append(source)
			anki['fields'].append(title)
			anki['fields'].append("[sound:%s]" % (url))
			anki['fields'].append("")
			anki['fields'].append("")
			anki['fields'].append(sentence)
			anki['fields'].append("")

			ankiList.append(anki)


logger = logging.getLogger("mylog")
logger.setLevel(logging.DEBUG)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler(".\\out\\logging.log")
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


bookList = []
ankiList = []

# Reading data
with open('.\\out\\books.json', 'r') as f:
	bookList = json.load(f)

ankijson(bookList, ankiList)
logger.info("\n\n ================ Totals: %d records ===============" % (len(ankiList)))
with open('.\\out\\ankiword.json', 'w') as f:
	json.dump(ankiList, f, indent = 4, sort_keys = True)
