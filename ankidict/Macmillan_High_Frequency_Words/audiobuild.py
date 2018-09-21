import pyttsx3
from pyttsx3 import voice
import time

import pyaudio
import wave



class TextSpeech(object):

    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.isSaying = True
     
    def SpeechAndSave(self, text, filename):
        isSaying = True

        def onStart(name):
            print('starting', name)
        def onWord(name, location, length):
            print('word', name, location, length)
        def onEnd(name, completed):
            print('finishing', name, completed)
            self.isSaying = False

        engine = pyttsx3.init()
        engine.connect('started-utterance', onStart)
        engine.connect('started-word', onWord)
        engine.connect('finished-utterance', onEnd)

        engine.setProperty('rate', 100)

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

if __name__ == '__main__':
    sp = TextSpeech()
    sp.SpeechAndSave('IT has made considerable changes to the world in 21st century.', 'output.mp3')
