iconfontjs2icons.py：
https://www.iconfont.cn 下载iconfont后，会产生iconfont.js文件。其中包括了图标的svg信息，并支持彩色。
这个工具会根据iconfont.js中的内容生成每个图标单独的svg文件。
命令：iconfontjs2icons.py iconfont.js

svgfont2icons.py：
https://www.iconfont.cn 下载iconfont后，会产生iconfont.svg字体文件。其中包括了图标的svg信息，但没有彩色。
这个工具会根据iconfont.svg中的内容生成每个图标单独的svg文件。
命令：svgfont2icons.py iconfont.svg

examples.js：
根据iconfont.css生成examples.html, 用来显示iconfont中有哪些图标。
命令：node examples.js
