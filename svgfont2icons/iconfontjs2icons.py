# -*- coding: utf-8 -*-
#python3
import re

# https://www.iconfont.cn 下载iconfont后，会产生iconfont.js文件。其中包括了图标的svg信息，并支持彩色。
# 这个工具会根据iconfont.js中的内容生成每个图标单独的svg文件。
# 命令：iconfontjs2icons.py iconfont.js

"""Converts iconfont.js to separate SVG icon files"""

__author__ = "Zhong Yuan Huan"
__copyright__ = "Copyright 2019, ZhongYuanHuan"
__email__ = "zhongyh6686@126.com"
__credits__ = "Zhong Yuan Huan zhongyh6686@126.com"

SVG_ICON_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Generator: Adobe Illustrator 17.0.2, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" 
   width="{{ width }}px" height="{{ height }}px" viewBox="0 0 {{ width }} {{ height }}" xml:space="preserve">
{{ path }}
</svg>
"""
import os
import sys
import argparse
from xml.etree import ElementTree

# 
# 
# 最重要的标签有三个font、font-face、glyph。
# 
# 我们要从这三个标签里获取的数据主要有：宽、高、基线偏移量、绘制数据
# 
# 数据获取：
# 
# 在font标签内获取默认字符宽度horiz-adv-x，例：<font id="fontawesomeregular" horiz-adv-x="1536" >
# 在font-face标签内获取默认高度units-per-em 和基准线上部ascent，基准线下部descent，例：<font-face units-per-em="1792" ascent="1536" descent="-256" />
# 在每个符号中查询是否存在特别的宽度horiz-adv-x，有则替换默认字符宽度。例：<glyph unicode="&#xf00b;" horiz-adv-x="1792"
# 在每个符号中获取绘制数据 d 。例：<glyph glyph-name="emo-wink2" unicode="&#xe802;" d="M664 800c-61 0-110-65-110-144 ........."
#
#    public static String makeSvgXml(DrawSize d) {
#        StringBuilder sb = new StringBuilder();
#        sb.append("<?xml version=\"1.0\" standalone=\"no\"?>\n");
#        sb.append("<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n");
#        sb.append("\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n");
#        sb.append("<svg width=\"").append(d.size).append("\" height=\"").append(d.size).append("\" viewBox=\"0 0 ").append(d.size).append(" ").append(d.size).append("\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n");
#        sb.append("<g class=\"transform-group\">\n");
#        sb.append("<g transform=\"translate(").append(d.x).append(", ").append(d.y).append(") scale(1, -1) scale(").append(d.scale).append(", ").append(d.scale).append(")\">");
#        sb.append(d.oSize.svgPath.replace("#737383", d.color));
#        sb.append("</g></g></svg>");
#        return sb.toString();
#    }
#

def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('iconfont_js_file', help="iconfont.js file", type=str)

    args = parser.parse_args(arguments)

    with open(args.iconfont_js_file, "r", encoding='UTF-8') as f:
        svg_data = f.read()
        svg_data = svg_data.replace("\n", "")
        svg_data = svg_data.strip()
        svg_data = re.findall(r'<svg>(.*?)</svg>', svg_data, re.S | re.M)
        svg_data = '<svg>' + svg_data[0] + '</svg>'
        # print(svg_data)

    xml_doc = ElementTree.fromstring(svg_data)

    if not os.path.exists('icons'):
        os.makedirs('icons')

    # 查找所有字符
    for symbol_node in xml_doc.findall('symbol'):
        id = symbol_node.get('id')
        viewBox = symbol_node.get('viewBox')
        box = viewBox.split()
        x = int(box[0])
        y = int(box[1])
        width = int(box[2])
        height = int(box[3])
        print(id)
        
        template = SVG_ICON_TEMPLATE.replace('{{ width }}', str(width)).replace('{{ height }}', str(height))
        template = template.replace('{{ position_x }}', str(x)).replace('{{ position_y }}', str(y))

        path = ''
        for path_node in symbol_node.findall('path'):
            # print(ElementTree.tostring(path_node, encoding='UTF-8'))
            path = path + str(ElementTree.tostring(path_node, encoding='UTF-8'), 'utf-8')
        template = template.replace('{{ path }}', path)

        icon_file = open(os.path.join('icons', id + '.svg'), 'w', encoding='UTF-8')
        icon_file.write(template)
        icon_file.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))