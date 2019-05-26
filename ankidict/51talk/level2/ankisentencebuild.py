#python3
import glob
import os.path
import logging
import re
from bs4 import BeautifulSoup
import json
import requests 
import uuid

def ankijson(bookList, ankiList):
	for i in range(0, len(bookList)):
		bookListItem = bookList[i]
		logger.info("\n\n=== Process %s ===" % bookListItem['params'])

		print(bookListItem['dialog_ref'])
		title = bookListItem['dialog_ref']['talk0']['title']
		url = bookListItem['dialog_ref']['talk0']['url']
		source = "%s_%s_%s"%(bookListItem['level_str'], bookListItem['unit_str'], bookListItem['lesson_str'])
		

		for j in range(0, len(title)):
			#{
			#	"__type__": "Note", 
			#	"data": "", 
			#	"fields": [
			#		"Listen and choice.[sound:d1_Good morning, Timmy. What time is it_.mp3]", 
			#		"Good morning, Timmy. What time is it?<br /><div>It's seven o'clock.</div><div>Good afternoon, Timmy. What time is it?</div><div>It's three o'clock.</div><div>Good evening, Dad. What time is it?</div><div>It's nine o'clock.</div><div>I am very tired.</div><div>It's time to go to bed.</div><div><br /></div>", 
			#		""
			#	], 
			#	"flags": 0, 
			#	"guid": "JX&od&TV1m", 
			#	"note_model_uuid": "5cf4f330-b243-11e8-91d4-180373427d85", 
			#	"tags": []
			#},
			anki = {}
			anki['__type__'] = "Note"
			anki['data'] = ""
			anki['flags'] = 0
			anki['note_model_uuid'] = "5cf4f330-b243-11e8-91d4-180373427d85"
			anki['tags'] = []
			anki['guid'] = str(uuid.uuid1())[0:8]

			anki['fields'] = []
			anki['fields'].append("%s_Sentence %d" % (source, j + 1))
			anki['fields'].append(title[j])
			anki['fields'].append("[sound:%s]" % (url[j]))

			options = "<div>%s</div>" % (title[j]) 
			for k in range(0, len(title)):
				if k != j:
					options += "<div>%s</div>" % (title[k]) 
			anki['fields'].append(options)

			sounds = "<div>[sound:%s]</div>" % (url[j])
			for k in range(0, len(title)):
				if k != j:
					sounds += "<div>[sound:%s]</div>" % (url[k])
			anki['fields'].append(sounds)
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
with open('.\\out\\ankisentence.json', 'w') as f:
	json.dump(ankiList, f, indent = 4, sort_keys = True)
