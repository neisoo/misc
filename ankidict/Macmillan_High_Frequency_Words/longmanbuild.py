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

outputPath = "./out"
audioPath = "./out/audio"
imagePath = "./out/image"
examplePath = "./out/example"

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

#从有道获取单词的基本信息，拼写，音标，释意，发音文件
def longmanwroddict(word=None):
    hl = hashlib.md5()
    result = {}
    url = 'https://www.ldoceonline.com/dictionary/%s' % (word)
    response = requests.post(url)
    soup = BeautifulSoup(response.text, "html.parser")
    keywordSpan = phrsListTabDiv.find(attrs={"data-src-mp3":"pagetitle"})
    if keywordSpan != None:
        keyword = str(keywordSpan.string)
        result['keyword'] = keyword.strip()
        
        hyphenateSpan = soup.find(attrs={"calll":"HYPHENATION"}) #音节切分
        if hyphenateSpan != None:
            hyphenate = str(hyphenateSpan.string)
            result['hyphenate'] = hyphenate

        #example = []
        #exampleSpan = soup.find_all(attrs={"title":"Play Example"})
        #for span in exampleSpan:
        #    sentence = str(span.parent.string).strip()
        #    soundurl = span.attrs('data-src-mp3')
        #    if type(soundurl) != None && len(sentence) > 0:
        #        md5 = hashlib.md5(sentence.encode(encoding='UTF-8')).hexdigest()
        #        filename = "%s.mp3" % (md5)
        #        r = requests.get(soundurl, timeout=10) #下载例句发音文件
        #        with open("%s/%s" % (filename), "wb") as code:
        #        result['sentence'].append("[sound:%s]%s" % (filename, sentence))
        #        result['soundurl'].append(filename)
                 
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
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        stream.stop_stream()
        stream.close()
        p.terminate()
        
def ankijson(srcData, dstData):
    notes = srcData['notes']
    
    for i in range(3008, len(notes)):
    #for i in range(0, 3):
        tryCount = 0

        while tryCount < 10:
            try:
                fields = notes[i]['fields']

                keyword = fields[0].split()[0].strip()
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
                            if url != "":
                                if url.startswith("http://"):
                                    print("3333333333333333333")
                                    #从网络下载
                                    r = requests.get(url)
                                    with open("%s/%s.jpg"%(imagePath, keyword), "wb") as code:
                                         code.write(r.content)
                                else:
                                    print("444444444444444")
                                    #从本地media目录复制
                                    open("%s/%s.jpg"%(imagePath, keyword), "wb").write(open("./media/%s" % (url), "rb").read())
                    print("555555555555555555")
                    word['image'] = "<img src=\"%s.jpg\" />" % keyword

                    # 单词例句和翻译
                    word['sentence'] = fields[4]
                    word['sentence_trans'] = fields[5]

                    # 单词发音
                    word['sound_en'] = "[sound:%s_1.mp3]" % (keyword)
                    word['sound_us'] = "[sound:%s_2.mp3]" % (keyword)
                    word['sound_se'] = "[sound:%s_3.mp3]" % (keyword)
                    
                    # 成生例名声音文件
                    #speech = TextSpeech()
                    #speech.SpeechAndSave(fields[4], "%s/%s_3.mp3" % (audioPath, keyword))

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
                    anki['guid'] = str(uuid.uuid1())[0:8]

                    anki['fields'] = []            
                    anki['fields'].append(word['keyword'])

                    if len(word['phonetic']) > 0: 
                        anki['fields'].append(word['phonetic'][0])
                    else:
                        anki['fields'].append("")

                    if len(word['phonetic']) > 1: 
                        anki['fields'].append(word['phonetic'][1])
                    else:
                        anki['fields'].append("")

                    anki['fields'].append(word['trans'])
                    anki['fields'].append(word['image'])
                    anki['fields'].append(word['sentence'])
                    anki['fields'].append(word['sentence_trans'])
                    anki['fields'].append(word['sound_en'])
                    anki['fields'].append(word['sound_us'])
                    anki['fields'].append(word['sound_se'])
                    break
                else:
                    print("####try count %d" % (tryCount))
                    tryCount = tryCount + 1
                    
            except AttributeError as err:
                print(err)
                print("****try count %d" % (tryCount))
                tryCount = tryCount + 1
            except ConnectionResetError as err:
                print(err)
                print("$$$$try count %d" % (tryCount))
                tryCount = tryCount + 1
                time.sleep(10)
            except KeyError as err:
                print(err)
                print("$$$$try count %d" % (tryCount))
                tryCount = tryCount + 1
            

        if tryCount >= 10:
            exit(0)
            
        dstData.append(anki)
        
        logger.info("%s," % (json.dumps(anki)))
        print(anki['fields'])
        print("=========================")
    
    #print(dstData)
    return

mkdir(outputPath)

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


srcData = {}
dstData = []

mkdir(audioPath)
mkdir(imagePath)
mkdir(examplePath)

# Reading data
with open('.\\m7000.json', 'r', encoding='UTF-8') as f:
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
