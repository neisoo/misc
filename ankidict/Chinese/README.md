1、tinxie.py从tinxie.json中读取词语列表，然后百度词语网站中获取数据。然后在out目录下生成output.json。output.json包含anki字典的词条数据。如果有无法识别的词条会记录在error.json中。

2、tinxiehz.py从tinxiehz.json中读取汉字列表，然后百度词语网站中获取数据。然后在out目录下生成output.json。output.json包含anki字典的词条数据。如果有无法识别的词条会记录在error.json中。

3、json输入目录 保存输入用的json文件。

4、json输出目录 保存输出的output文件。

5、记忆库目录是生成好的anki词典文件，通过CrowdAnki插件导入或导出。

关于汉字发音网址：

https://ss0.baidu.com/6KAZsjip0QIZ8tyhnq/text2audio?tex=看(kan4)见(jian4)&cuid=dict&lan=ZH&ctp=1&pdt=30&vol=9&spd=4

https://ss0.baidu.com/6KAZsjip0QIZ8tyhnq/text2audio?tex=看见&cuid=dict&lan=ZH&ctp=1&pdt=30&vol=9&spd=4

替换上面的tex参数就可以更改声音。
