m7000build.py 根据原有的麦克米伦字典m7000.json中单词，分别从有道、牛津、朗文词典网站抓取单词数据。

1.从https://dictionary.cambridge.org/dictionary/english剑桥牛津在线词典中获取单词的英美音标，这个音标带有音节切分。
2.从https://www.ldoceonline.com/dictionary朗文在线词典中获取单词的拼写音节切分，例句，例句音频。
3.从http://dict.youdao.com/w/%s/#keyfrom=dict2.top有道词典中获取单词的中文释意，英美音标发音文件。
4.根据原来的字典例图链接，从百词斩下载例图。为例图句子自动生成例图句子的机器语音。
5.朗文例句的翻译从http://fanyi.youdao.com/translate自动生成机器翻译。
6.audiobuild.py可以自动生成句子的机器发音。
