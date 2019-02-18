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

import pyttsx3
from pyttsx3 import voice
import pyaudio
import wave

import time
import hashlib
from pydub import AudioSegment

outputPath = "./out"
audioPath = "./out/audio"
imagePath = "./out/image"
        
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

def translate(word=None):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    key={
    'type':"AUTO",
    'i':word,
    "doctype":"json",
    "version":"2.1",
    "keyfrom":"fanyi.web",
    "ue":"UTF-8",
    "action":"FY_BY_CLICKBUTTON",
    "typoResult":"true"
    }  
    #key这个字典为发送给有道词典服务器的内容，里面的i就是我们需要翻译的内容。此处直接调用word变量。
    response = requests.post(url,data=key,timeout=5)
    result = json.loads(response.text)
    return result['translateResult'][0][0]['tgt']

#从剑桥牛津在线词典中获取单词的音标切分数据
def cambridgewroddict(word=None):
    result = {}
    url = 'https://dictionary.cambridge.org/dictionary/english/%s' % (word)
    print("b11111111111111111111111")
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'} #伪装成google浏览器,因为服务器根据 UA 来判断拒绝了 python 爬虫。
    response = requests.post(url, headers=headers, timeout=5)
    print("b22222222222222222222222")

    soup = BeautifulSoup(response.text, "html.parser")
    posheaderDiv = soup.find(attrs={"class":"pos-header"})
    if not posheaderDiv is None:    
        keywordSpan = posheaderDiv.find(attrs={"class":"hw"})
        if type(keywordSpan) != None:
            keyword = str(keywordSpan.string)
            result['keyword'] = keyword.strip()
            
            phonetic = []
            phoneticSpan = posheaderDiv.find_all(attrs={"class":"ipa"})
            for span in phoneticSpan:
                phonetic.append(span.get_text())
            
            result['phonetic'] = phonetic

    print("b9999999999999999999")        
    return result
 
#从朗文在线词典中获取单词的切分数据，例句
def longmanwroddict(word=None, needExample=False, maxExample=3):
    result = {}
    url = 'https://www.ldoceonline.com/dictionary/%s' % (word.replace(" ", "-"))
    #url = 'http://www.ldoceonline.com/dictionary/%s' % (word)    
    print("a11111111111111111111111_%s"%(word))
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'} #伪装成google浏览器,因为服务器根据 UA 来判断拒绝了 python 爬虫。
    response = requests.post(url, headers=headers, timeout=5)
    print("a22222222222222222222222")

    soup = BeautifulSoup(response.text, "html.parser")
    keywordSpan = soup.find(attrs={"class":"pagetitle"})
    if not keywordSpan is None:
        print("a3333333333333333")
        keyword = str(keywordSpan.string)
        print("a44444444444444444%s"%keyword)
        result['keyword'] = keyword.strip()
        
        hyphenateSpan = soup.find(attrs={"class":"HYPHENATION"}) #音节切分
        if hyphenateSpan != None:
            hyphenate = str(hyphenateSpan.string)
            result['hyphenate'] = hyphenate

        if needExample:
            i = 1
            result["example"] = []
            result["example_trans"] = []
            result["example_sound"] = []
            exampleSpan = soup.find_all(attrs={"title":"Play Example"})
            for span in exampleSpan:
                sentence = str(span.parent.get_text()).strip()
                soundurl = span.attrs['data-src-mp3']
                if (not soundurl is None) and len(sentence) > 0:
                    md5 = hashlib.md5(sentence.encode(encoding='UTF-8')).hexdigest()
                    print("a555555555555555555")
                    r = requests.get(soundurl, headers=headers, timeout=10) #下载例句发音文件
                    print("a6666666666666666666")
                    if r.status_code == 200:
                        with open("%s/longman_%s.mp3" % (audioPath, md5), "wb") as code:
                            code.write(r.content)
                            result["example"].append(sentence)
                            result["example_trans"].append(translate(sentence))
                            result["example_sound"].append("[sound:longman_%s.mp3]" % (md5))
                            i = i + 1
                            if i > maxExample:
                                break
    return result
    
#从有道获取单词的基本信息，拼写，音标，释意，发音文件
def wroddict(word=None):
    result = {}
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'} #伪装成google浏览器,因为服务器根据 UA 来判断拒绝了 python 爬虫。

    #url = 'http://dict.youdao.com/search?q=%s' % (word)
    url = 'http://dict.youdao.com/w/%s/#keyfrom=dict2.top' % (word)
    print("aaaaaaaaaaaaaaaaaa%s"%(word))
    response = requests.post(url, headers=headers, timeout=5)
    print("bbbbbbbbbbbbbbbbbbb")
    soup = BeautifulSoup(response.text, "html.parser")
    phrsListTabDiv = soup.find(attrs={"id":"phrsListTab"})
    if not phrsListTabDiv is None:
        keywordSpan = phrsListTabDiv.find(attrs={"class":"keyword"})
        transDiv = phrsListTabDiv.find(attrs={"class":"trans-container"}).ul #翻译
        baavDiv = phrsListTabDiv.find(attrs={"class":"baav"}) # 发音

        keyword = str(keywordSpan.string)
        trans = str(transDiv).replace("\n","")
        
        #优先使用牛津中的音标，有音节切分。没有的话就使用有道词典的音标
        cambridge = cambridgewroddict(word)
        result['phonetic'] = cambridge.get('phonetic', [])
        if len(result['phonetic']) == 0:
            phonetic = []
            phoneticSpan = baavDiv.find_all(attrs={"class":"phonetic"})
            for span in phoneticSpan:
                strTmp = str(span.string)
                strTmp = strTmp.replace("[", "")
                strTmp = strTmp.replace("]", "")
                phonetic.append(strTmp)
            result['phonetic'] = phonetic

        audioPath = "./out/audio"
        mkdir(audioPath)
        
        #下载单词发音文件
        print("cccccccccccccccc%s"%(keyword))
        r = requests.get("http://dict.youdao.com/dictvoice?audio=%s&type=1" % keyword, headers=headers, timeout=10) #英音
        print("ddddddddddddddddd")
        with open("%s/%s_1.mp3"%(audioPath, keyword), "wb") as code:            
            code.write(r.content)
            result['sound_en'] = "[sound:%s_1.mp3]" % (keyword)

        print("eeeeeeeeeeeeeee")
        r = requests.get("http://dict.youdao.com/dictvoice?audio=%s&type=2" % keyword, headers=headers, timeout=10) #美音
        with open("%s/%s_2.mp3"%(audioPath, keyword), "wb") as code:
            code.write(r.content)
            result['sound_us'] = "[sound:%s_2.mp3]" % (keyword)
        print("ffffffffffffffff")

        result['keyword'] = keyword
        result['trans'] = trans

        longman = longmanwroddict(keyword, True, 3)
        result['hyphenate'] = longman.get('hyphenate', "")
        
        if len(longman.get('example', [""])) > 0:
            result['example_1'] = longman.get('example', [""])[0]
            result['example_1_trans'] = longman.get('example_trans', [""])[0]
            result['example_1_sound'] = longman.get('example_sound', [""])[0]

        if len(longman.get('example', [""])) > 1:
            result['example_2'] = longman.get('example', ["",""])[1]
            result['example_2_trans'] = longman.get('example_trans', ["",""])[1]
            result['example_2_sound'] = longman.get('example_sound', ["",""])[1]

        if len(longman.get('example', [""])) > 2:
            result['example_3'] = longman.get('example', ["","",""])[2]
            result['example_3_trans'] = longman.get('example_trans', ["","",""])[2]
            result['example_3_sound'] = longman.get('example_sound', ["","",""])[2]

        #print("=====================")
        #print(result)
                 
    return result

class TextSpeech(object):

    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.isSaying = True
        self.text = ""
     
    def SpeechAndSave(self, text, filename):
        self.isSaying = True
        self.text = text

        def onStart(name):
            print('starting')
        def onWord(name, location, length):
            print("word: %s" % (self.text[location : location + length]))
        def onEnd(name, completed):
            print('finishing')
            self.isSaying = False

        engine = pyttsx3.init()
        engine.connect('started-utterance', onStart)
        engine.connect('started-word', onWord)
        engine.connect('finished-utterance', onEnd)

        engine.setProperty('rate', 120)

        #播放时录制声音
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        #开始播放
        self.isSaying = True
        engine.say(text)
        engine.startLoop(False)

        #一边播放一边录音
        frames = []
        while self.isSaying:
            engine.iterate()
            data = stream.read(self.CHUNK)
            frames.append(data)

        #录音结束    
        engine.endLoop()
            
        #保存到文件中
        wf = wave.open("./out/temp.wav", 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        #转成mp3文件
        song = AudioSegment.from_wav("./out/temp.wav")
        song.export(filename, format="mp3")
    
        stream.stop_stream()
        stream.close()
        p.terminate()
        
def ankijson(srcData, dstData):
    notes = srcData['notes']
    
    for i in range(0, len(notes)):
    #for i in range(0, 3):
        tryCount = 0

        while tryCount < 10:
            try:
                fields = notes[i]['fields']

                keyword = fields[0].split('[')[0].strip()
                print("%d=%s=====================" % (i, keyword))
                
                word = wroddict(keyword)
                print("11111111111111111111")
                if type(word['keyword']) != None:
                
                    keyword = word['keyword']
                    
                    # 下载单词图片
                    if fields[3] != "":
                        print("2222222222222222222")
                        soup = BeautifulSoup(fields[3], "html.parser")
                        images = soup.find_all('img')
                        for image in images:
                            url = image["src"]

                            # windows 特殊文件名
                            imageName = keyword
                            if imageName in ['con', 'aux', 'nul']:
                                imageName = "%s_" % (imageName)

                            if url != "":
                                if url.startswith("http://"):
                                    print("3333333333333333333")
                                    #从网络下载
                                    r = requests.get(url)
                                    with open("%s/%s.jpg"%(imagePath, imageName), "wb") as code:
                                         code.write(r.content)
                                         word['image'] = "<img src=\"%s.jpg\" />" % imageName
                                elif os.path.exists("./media/%s" % (url)):
                                    print("444444444444444")
                                    #从本地media目录复制
                                    open("%s/%s.jpg"%(imagePath, imageName), "wb").write(open("./media/%s" % (url), "rb").read())
                                    word['image'] = "<img src=\"%s.jpg\" />" % imageName
                                else :
                                    word['image'] = ""
                        print("555555555555555555")
                    else:
                        word['image'] = ""
                    

                    # 单词例句和翻译
                    if len(fields[4]) != 0:
                        word['sentence'] = fields[4]
                        word['sentence_trans'] = fields[5]

                        # 成生例名声音文件
                        speech = TextSpeech()
                        speech.SpeechAndSave(fields[4], "%s/%s_3.mp3" % (audioPath, keyword))
                        word['sentence_sound'] = "[sound:%s_3.mp3]" % (keyword)

                    """
                    "__type__": "Note", 
                    "data": "", 
                    "fields": [
                        "restructure [sound:youdao-6575f2be-2c2e7b2c-928f2452-67cb03c3-1eee6a85.mp3]", 
                        "<div class=\"hd_prUS\">美&#160;[.ri'strʌktʃər] </div>", 
                        "v. 重建，重造，改组", 
                        "<img src=\"http://assets.baicizhan.com/r/5_49_129_20161214160219_347_c.jpg\">", 
                        "Due to the change of personnel, we must restructure the management team this week.", 
                        "因为人事变动，我们需要在一周之内重组管理层。"
                    ], 
                    "flags": 0, 
                    "guid": "oA?<c8<v?)", 
                    "note_model_uuid": "b5c6950f-b705-11e8-a891-180373427d85", 
                    "tags": []
                    """
                    
                    anki = {}
                    anki['__type__'] = "Note"
                    anki['data'] = ""
                    anki['flags'] = 0
                    anki['note_model_uuid'] = "e21b0d8f-b1b9-11e8-a35c-180373427d85"
                    anki['tags'] = []
                    anki['guid'] = str(uuid.uuid1())#str(uuid.uuid1())[0:8]

                    anki['fields'] = []
                    anki['fields'].append(word['keyword'])
                    anki['fields'].append(word['hyphenate'])

                    if len(word['phonetic']) > 0: 
                        anki['fields'].append(word['phonetic'][0])
                    else:
                        anki['fields'].append("")

                    if len(word['phonetic']) > 1: 
                        anki['fields'].append(word['phonetic'][1])
                    else:
                        anki['fields'].append("")

                    anki['fields'].append(word.get('sound_en', ""))
                    anki['fields'].append(word.get('sound_us', ""))
                    anki['fields'].append(word.get('trans', ""))
                    anki['fields'].append(word.get('image', ""))
                    anki['fields'].append(word.get('sentence', ""))
                    anki['fields'].append(word.get('sentence_trans', ""))
                    anki['fields'].append(word.get('sentence_sound', ""))
                    
                    anki['fields'].append(word.get('example_1', ""))
                    anki['fields'].append(word.get('example_1_trans', ""))
                    anki['fields'].append(word.get('example_1_sound', ""))
                    anki['fields'].append(word.get('example_2', ""))
                    anki['fields'].append(word.get('example_2_trans', ""))
                    anki['fields'].append(word.get('example_2_sound', ""))
                    anki['fields'].append(word.get('example_3', ""))
                    anki['fields'].append(word.get('example_3_trans', ""))
                    anki['fields'].append(word.get('example_3_sound', ""))

                    break
                else:
                    print("####try count %d" % (tryCount))
                    tryCount = tryCount + 1
                    
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
        if tryCount >= 20:
            exit(0)
            
        dstData.append(anki)
        
        logger.info("%s," % (json.dumps(anki, ensure_ascii=False, indent=4)))
        print(anki['fields'])
        print("=========================")
    
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

mkdir(audioPath)
mkdir(imagePath)

# Reading data
with open('.\\m7000_one.json', 'r', encoding='UTF-8') as f:
    srcData = json.load(f)

#dstJsonFileName = '.\\out\\output.json'
#isExists=os.path.exists(dstJsonFileName)
#if isExists:
#    with open(dstJsonFileName, 'r', encoding='UTF-8') as f:
#        dstData = json.load(f)

ankijson(srcData, dstData)
logger.info("\n\n ================ Totals: %d records ===============" % (len(dstData)))
with open('.\\out\\output.json', 'w') as f:
    json.dump(dstData, f, indent = 4, sort_keys = True)
