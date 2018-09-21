#python3
import glob
import os.path
import logging
import re
from bs4 import BeautifulSoup
import json
import requests 


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

def getdata(filename, bookList):
	logger.info("\n\n=== Process %s ===" % filename)

	with open(filename, encoding='utf-8') as file_object:
		contents = file_object.read()
	
		#data = """
		#<script>
		#var www_url = "//static.51talk.com";
		#var word_ref = [{"title":"thirteen","url":"0a0f038f0844a6732c61e49e6df8d6f4_1611153c4.mp3","sentence1":"There are thirteen apples.","sentence1_url":"ac34af028f53e9cb0cd1e99ba0d501e7_16111527b.mp3","sentence2":"I am thirteen years old.","sentence2_url":"497139987e5f406aa003522aee97a3bf_161115b83.mp3"},{"title":"fourteen","url":"f42cb9655182b4ecaea608b78ff886ad_161115928.mp3","sentence1":"He works fourteen hours a day.","sentence1_url":"b4c485b42e6dd2a663c848823d24db71_161115449.mp3","sentence2":"I started playing the guitar when I was fourteen.","sentence2_url":"d6e88218ed295f6c2594a98144fddee4_1611150b7.mp3"},{"title":"fifteen","url":"62c5e100008bbd78f30f9abb7ac2f646_16111557d.mp3","sentence1":"I live in a village fifteen miles south of California.","sentence1_url":"9758cf2260a42908a43e2940ed536c21_161115b80.mp3","sentence2":"They met when she was fifteen.","sentence2_url":"1048305286704b86005e464fafa3f2c9_1611156e1.mp3"}];
		#var dialog_ref = {"talk0":{"title":["Wow, there are many animals on the farm.","Yes, let\u2018s see how many there are.","How many cows are there on the farm?","There are thirteen cows on the farm.","How many horses are there on the farm?","There are fourteen horses on the farm.","How many ducks are there on the farm?","There are fifteen ducks on the farm."],"url":["d1d574c9cf9766c73c46def116cab224_1611241de.mp3","73d089477c78a841a2cb0396ffc631f1_1612026e9.mp3","cdbc640e5acc63214bec791d896d8531_161124021.mp3","272cd4cf87af5c01da4cb14f9834e495_1612028a5.mp3","42e014710f8f33e06f06921b4eecb416_1611248cd.mp3","e45b546782a7221d88f7d595befb8190_1611264f5.mp3","0a3a16ed70d75a5642e76a92546f13c2_17020605c.mp3","1277918da877e3bbd37fb857d913b56e_1611252bf.mp3"]}};
		#var sentence_ref = 0;
		#var params = 776931;
		#var snum = "U23057131136";
		#var video_url = "https://static.51talk.com/upload/efl_video/prepar/08c433c0f9aa21a45c233c2cb54796ae_161201979.mp4";
		#</script>
		#"""
	
		soup = BeautifulSoup(contents, "html.parser")
		pattern = re.compile(r"var www_url = \"(.*?)\";$", re.MULTILINE | re.DOTALL)
		script = soup.find("script", text=pattern)
		logger.info("www_url=%s" % (pattern.search(script.text).group(1)))
		var_www_url_str = pattern.search(script.text).group(1)
		
		pattern = re.compile(r"var word_ref = (.*?);$", re.MULTILINE | re.DOTALL)
		script = soup.find("script", text=pattern)
		logger.info("word_ref=%s" % (pattern.search(script.text).group(1)))
		var_word_ref_str = pattern.search(script.text).group(1)

		pattern = re.compile(r"var dialog_ref = (.*?);$", re.MULTILINE | re.DOTALL)
		script = soup.find("script", text=pattern)
		logger.info("dialog_ref=%s" % (pattern.search(script.text).group(1)))
		var_dialog_ref_str = pattern.search(script.text).group(1)

		pattern = re.compile(r"var sentence_ref = (.*?);$", re.MULTILINE | re.DOTALL)
		script = soup.find("script", text=pattern)
		logger.info("sentence_ref=%s" % (pattern.search(script.text).group(1)))
		var_sentence_ref_str = pattern.search(script.text).group(1)

		pattern = re.compile(r"var params = (.*?);$", re.MULTILINE | re.DOTALL)
		script = soup.find("script", text=pattern)
		logger.info("params=%s" % (pattern.search(script.text).group(1)))
		var_params_str = pattern.search(script.text).group(1)

		pattern = re.compile(r"var snum = \"(.*?)\";$", re.MULTILINE | re.DOTALL)
		script = soup.find("script", text=pattern)
		logger.info("snum=%s" % (pattern.search(script.text).group(1)))
		var_snum_str = pattern.search(script.text).group(1)

		pattern = re.compile(r"var video_url = \"(.*?)\";$", re.MULTILINE | re.DOTALL)
		script = soup.find("script", text=pattern)
		logger.info("video_url=%s" % (pattern.search(script.text).group(1)))
		var_video_url_str = pattern.search(script.text).group(1)

		bookListItem = {}
		bookListItem['www_url'] = var_www_url_str;
		bookListItem['word_ref'] = json.loads(var_word_ref_str)
		bookListItem['dialog_ref'] = json.loads(var_dialog_ref_str)
		bookListItem['sentence_ref'] = int(var_sentence_ref_str)
		bookListItem['params'] = int(var_params_str)
		bookListItem['snum'] = var_snum_str;
		bookListItem['video_url'] = var_video_url_str;
		bookListItem['book_url'] = "http://www.51talk.com/download/book?course_id=%d"%(bookListItem['params']);

		pattern = re.compile(r"Level (.*?)", re.MULTILINE | re.DOTALL)
		script = soup.find("span", title=pattern)
		logger.info("level_str=%s" % (script.string))
		level_str = script.string
		bookListItem['level_str'] = level_str

		pattern = re.compile(r"Unit (.*?)", re.MULTILINE | re.DOTALL)
		script = soup.find("span", title=pattern)
		logger.info("unit_str=%s" % (script.string))
		unit_str = script.string
		bookListItem['unit_str'] = unit_str

		pattern = re.compile(r"Lesson (.*?)", re.MULTILINE | re.DOTALL)
		script = soup.find("span", title=pattern)
		logger.info("lesson_str=%s" % (script.string))
		lesson_str = script.string
		bookListItem['lesson_str'] = lesson_str

		bookList.append(bookListItem)
		logger.info(bookListItem)

def downloaddata(bookList):
	mkdir("./out/upload/efl_video/prepar")
	mkdir("./out/upload/efl_audio/prepar")
	mkdir("./out/download/book")
	for i in range(0, len(bookList)):
		bookListItem = bookList[i]
		
		logger.info("\n\n=== Process %s ===" % bookListItem['params'])

		if bookListItem['video_url']:
			video_url = bookListItem['video_url']
			filename = os.path.basename(video_url)
			logger.info("\n\n=== download video: %s ===" % filename)
			r = requests.get(video_url) 
			with open("./out/upload/efl_video/prepar/%s"%(filename), "wb") as code:
				 code.write(r.content)

		#book_url = "http://www.51talk.com/download/book?course_id=793981"#bookListItem['book_url']
		#r = requests.get(book_url) 
		#with open("./out/download/book/%d.pdf"%(bookListItem['params']), "wb") as code:
		#	 code.write(r.content)
		dialog_ref = bookListItem['dialog_ref']
		for j in range(0, len(dialog_ref['talk0']['url'])):
			if dialog_ref['talk0']['url'][j]:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (dialog_ref['talk0']['url'][j])
				filename = os.path.basename(url)
				logger.info("\n\n=== download dialog: %s ===" % filename)
				r = requests.get(url) 
				with open("./out/upload/efl_audio/prepar/%s"%(filename), "wb") as code:
					 code.write(r.content)

		word_ref = bookListItem['word_ref']
		for j in range(0, len(word_ref)):
			if word_ref[j]['url']:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (word_ref[j]['url'])
				filename = os.path.basename(url)
				logger.info("\n\n=== download word: %s ===" % filename)
				r = requests.get(url) 
				with open("./out/upload/efl_audio/prepar/%s"%(filename), "wb") as code:
					 code.write(r.content)

			if word_ref[j]['sentence1_url']:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (word_ref[j]['sentence1_url'])
				filename = os.path.basename(url)
				logger.info("\n\n=== download sentence1: %s ===" % filename)
				r = requests.get(url) 
				with open("./out/upload/efl_audio/prepar/%s"%(filename), "wb") as code:
					 code.write(r.content)

			if word_ref[j]['sentence2_url']:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (word_ref[j]['sentence2_url'])
				filename = os.path.basename(url)
				logger.info("\n\n=== download sentence2: %s ===" % filename)
				r = requests.get(url) 
				with open("./out/upload/efl_audio/prepar/%s"%(filename), "wb") as code:
					 code.write(r.content)

def downloaddata2(bookList):
	for i in range(0, len(bookList)):
		bookListItem = bookList[i]
		
		logger.info("\n\n=== Process %s ===" % bookListItem['params'])

		dirname = "./out/my51talk/%s/%s"%(validateTitle(bookListItem['unit_str']), validateTitle(bookListItem['lesson_str']))
		mkdir(dirname)

		if bookListItem['video_url']:
			video_url = bookListItem['video_url']
			filename = os.path.basename(video_url)
			logger.info("\n\n=== download video: %s ===" % filename)
			r = requests.get(video_url) 
			with open("%s/%s"%(dirname, filename), "wb") as code:
				 code.write(r.content)

		#book_url = "http://www.51talk.com/download/book?course_id=793981"#bookListItem['book_url']
		#r = requests.get(book_url) 
		#with open("./out/download/book/%d.pdf"%(bookListItem['params']), "wb") as code:
		#	 code.write(r.content)
		dialog_ref = bookListItem['dialog_ref']
		for j in range(0, len(dialog_ref['talk0']['url'])):
			if dialog_ref['talk0']['url'][j]:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (dialog_ref['talk0']['url'][j])
				filename = os.path.basename(url)
				logger.info("\n\n=== download dialog: %s ===" % filename)
				r = requests.get(url) 
				with open("%s/%s"%(dirname, filename), "wb") as code:
					 code.write(r.content)

		word_ref = bookListItem['word_ref']
		for j in range(0, len(word_ref)):
			if word_ref[j]['url']:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (word_ref[j]['url'])
				filename = os.path.basename(url)
				logger.info("\n\n=== download word: %s ===" % filename)
				r = requests.get(url) 
				with open("%s/%s"%(dirname, filename), "wb") as code:
					 code.write(r.content)

			if word_ref[j]['sentence1_url']:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (word_ref[j]['sentence1_url'])
				filename = os.path.basename(url)
				logger.info("\n\n=== download sentence1: %s ===" % filename)
				r = requests.get(url) 
				with open("%s/%s"%(dirname, filename), "wb") as code:
					 code.write(r.content)

			if word_ref[j]['sentence2_url']:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (word_ref[j]['sentence2_url'])
				filename = os.path.basename(url)
				logger.info("\n\n=== download sentence2: %s ===" % filename)
				r = requests.get(url) 
				with open("%s/%s"%(dirname, filename), "wb") as code:
					 code.write(r.content)

def downloaddata3(bookList):
	for i in range(0, len(bookList)):
		bookListItem = bookList[i]
		
		logger.info("\n\n=== Process %s ===" % bookListItem['params'])

		dirname = "./out/51talk_mankind/%s/%s"%(validateTitle(bookListItem['unit_str']), validateTitle(bookListItem['lesson_str']))
		mkdir(dirname)

		if bookListItem['video_url']:
			video_url = bookListItem['video_url']
			filename = os.path.basename(video_url)
			logger.info("\n\n=== download video: %s ===" % filename)
			r = requests.get(video_url) 
			with open("%s/preview_video.mp4"%(dirname), "wb") as code:
				 code.write(r.content)

		#book_url = "http://www.51talk.com/download/book?course_id=793981"#bookListItem['book_url']
		#r = requests.get(book_url) 
		#with open("./out/download/book/%d.pdf"%(bookListItem['params']), "wb") as code:
		#	 code.write(r.content)
		dialog_ref = bookListItem['dialog_ref']
		for j in range(0, len(dialog_ref['talk0']['url'])):
			if dialog_ref['talk0']['url'][j]:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (dialog_ref['talk0']['url'][j])
				filename = os.path.basename(url)
				logger.info("\n\n=== download dialog: %s ===" % filename)
				r = requests.get(url) 
				with open("%s/d%d_%s.mp3"%(dirname, j+1, validateTitle(dialog_ref['talk0']['title'][j])), "wb") as code:
					 code.write(r.content)

		word_ref = bookListItem['word_ref']
		for j in range(0, len(word_ref)):
			if word_ref[j]['url']:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (word_ref[j]['url'])
				filename = os.path.basename(url)
				logger.info("\n\n=== download word: %s ===" % filename)
				r = requests.get(url) 
				with open("%s/w%d_%s.mp3"%(dirname, j+1, validateTitle(word_ref[j]['title'])), "wb") as code:
					 code.write(r.content)

			if word_ref[j]['sentence1_url']:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (word_ref[j]['sentence1_url'])
				filename = os.path.basename(url)
				logger.info("\n\n=== download sentence1: %s ===" % filename)
				r = requests.get(url) 
				with open("%s/w%d_s1_%s_%s.mp3"%(dirname, j+1, validateTitle(word_ref[j]['title']), validateTitle(word_ref[j]['sentence1'])), "wb") as code:
					 code.write(r.content)

			if word_ref[j]['sentence2_url']:
				url = "http://static.51talk.com/upload/efl_audio/prepar/%s" % (word_ref[j]['sentence2_url'])
				filename = os.path.basename(url)
				logger.info("\n\n=== download sentence2: %s ===" % filename)
				r = requests.get(url) 
				with open("%s/w%d_s2_%s_%s.mp3"%(dirname, j+1, validateTitle(word_ref[j]['title']), validateTitle(word_ref[j]['sentence2'])), "wb") as code:
					 code.write(r.content)

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
####html_path = glob.glob('.\\51talk\\*.html')
####i=1
####for each in html_path:
####	logger.info(each)
####	getdata(each, bookList)
####	i=i+1
####
####logger.info("\n\n ========== Result ==============")
####logger.info(bookList)
####
####with open('.\\out\\books.json', 'w') as f:
####	json.dump(bookList, f)

# Reading data back
with open('.\\out\\books.json', 'r') as f:
	bookList = json.load(f)
	
#downloaddata(bookList)
downloaddata3(bookList)
#img = cv2.imread('.\\test.jpg')
#img = addRoundCorner(img, 100, (255, 0, 0))
#cv2.imwrite('.\\reslut.jpg', img)
