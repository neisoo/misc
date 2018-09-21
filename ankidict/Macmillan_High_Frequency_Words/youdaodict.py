#调用有道词典的web接口抓取单词
#coding: utf-8
import requests
import json
import re
from bs4 import BeautifulSoup
import os.path

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

def wroddict(word=None):
    result = {}
    url = 'http://dict.youdao.com/search?q=%s' % (word)
    #key这个字典为发送给有道词典服务器的内容，里面的i就是我们需要翻译的内容。此处直接调用word变量。
    response = requests.post(url)
    #print(response.text)
    
    soup = BeautifulSoup(response.text, "html.parser")
    phrsListTabDiv = soup.find(attrs={"id":"phrsListTab"})
    if phrsListTabDiv != None:
        keywordSpan = phrsListTabDiv.find(attrs={"class":"keyword"})
        transDiv = phrsListTabDiv.find(attrs={"class":"trans-container"}).ul #翻译
        baavDiv = phrsListTabDiv.find(attrs={"class":"baav"}) # 发音

        print("========================")
        
        keyword = str(keywordSpan.string)
        #print("word:%s" % (keyword))
        
        trans = str(transDiv).replace("\n","")
        #print("trans:%s" % (trans))
        
        phonetic = []
        phoneticSpan = baavDiv.find_all(attrs={"class":"phonetic"})
        for span in phoneticSpan:
            strTmp = str(span.string)
            strTmp = strTmp.replace("[", "")
            strTmp = strTmp.replace("]", "")
            phonetic.append(strTmp)
        #print("phonetic:%s" % (phonetic))

        #print("========================")
        
        audioPath = "./out/audio"
        mkdir(audioPath)
        
        #下载单词发音文件
        r = requests.get("http://dict.youdao.com/dictvoice?audio=%s&type=1" % word) #英音
        with open("%s/%s_1.mp3"%(audioPath, word), "wb") as code:
             code.write(r.content)
        r = requests.get("http://dict.youdao.com/dictvoice?audio=%s&type=2" % word) #美音
        with open("%s/%s_2.mp3"%(audioPath, word), "wb") as code:
             code.write(r.content)
        
        result['keyword'] = keyword
        result['phonetic'] = phonetic
        result['trans'] = trans
        
        print(result)
        
         
    return response

def get_result(li=None):
    result = json.loads(li.text)
    print ("输入的词为：%s" % result['translateResult'][0][0]['src'])
    print ("翻译结果为：%s" % result['translateResult'][0][0]['tgt'])

def main():
    print ("本程序调用有道词典的API进行翻译，可达到以下效果：")
    print ("外文-->中文")
    print ("中文-->英文")
    word = input('请输入你想要翻译的词或句：')
    list_trans = wroddict(word)
    #get=get_result(list_trans)

if __name__ == '__main__':
    main()