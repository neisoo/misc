# -*- coding: utf-8 -*-
#python3

# https://www.iconfont.cn 下载iconfont后，会产生iconfont.svg字体文件。其中包括了图标的svg信息，但没有彩色。
# 这个工具会根据iconfont.svg中的内容生成每个图标单独的svg文件。
# 命令：svgfont2icons.py iconfont.svg

"""Converts SVG fonts to separate SVG icon files"""

__author__ = "Aidas Bendoraitis"
__copyright__ = "Copyright 2015, Berlin"
__email__ = "aidas@bendoraitis.lt"
__credits__ = "Thomas Helbig (http://www.dergraph.com / http://www.neuedeutsche.com)"


# transform 表示偏移，scale表示缩放

SVG_ICON_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Generator: Adobe Illustrator 17.0.2, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" 
   width="{{ width }}px" height="{{ height }}px" viewBox="0 0 {{ width }} {{ height }}" xml:space="preserve">
<path d="{{ icon_path }}" transform="scale(1,-1) translate({{ position_x }}, {{ position_y }})" />
</svg>
"""
import os
import sys
import argparse
from xml.etree import ElementTree


def parse_glyphs_file(f):
    mapper = {}
    glyphname = uni = ""
    for line in f.readlines():
        line = line.replace('\n', '')
        if line.startswith("glyphname"):
            _, glyphname = line.split(' = ')
            glyphname = glyphname.replace(';', '').replace('"', '').replace("'", '')
        if line.startswith("unicode"):
            _, uni = line.split(' = ')
            uni = uni.replace(';', '')
        if glyphname and uni:
            mapper['uni' + uni] = glyphname
            glyphname = uni = ""
    return mapper

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
    parser.add_argument('svg_font_file', help="SVG input file", type=str)
    parser.add_argument('glyphs_font_file', nargs='?', help="Glyphs input file", type=str)
    parser.add_argument('--padding', nargs='?', help="Glyph padding", type=int, default=0)

    args = parser.parse_args(arguments)

    with open(args.svg_font_file, "r") as f:
        svg_data = f.read()

    name_mapper = {}
    if args.glyphs_font_file:
        with open(args.glyphs_font_file, "r") as f:
            name_mapper = parse_glyphs_file(f)

    xml_doc = ElementTree.fromstring(svg_data)

    if not os.path.exists('icons'):
        os.makedirs('icons')

    # 查找
    font = xml_doc.find('defs/font')
    fontface = xml_doc.find('defs/font/font-face')
    print(font.attrib['horiz-adv-x'])
    print(fontface.attrib['units-per-em'])
    print(fontface.attrib['ascent'])
    
    padding = args.padding

    for glyph_node in xml_doc.findall('defs/font/glyph'):
    
        size = int(font.attrib['horiz-adv-x'])
        if (glyph_node.get('horiz-adv-x')) :
            size = int(glyph_node.get('horiz-adv-x'))
        print("size=%d" % size)
        
        template = SVG_ICON_TEMPLATE.replace('{{ width }}', str(size + 2 * padding)).replace('{{ height }}', str(size + 2 * padding))
        template = template.replace('{{ position_x }}', str(padding)).replace('{{ position_y }}', str(-size - padding - int(fontface.attrib['descent'])))

        glyph_name = glyph_node.get('glyph-name').replace('.', '')
        glyph_path = glyph_node.get('d')
        glyph_unicode = glyph_node.get('unicode')
        glyph_unicode = '%x' % ord(glyph_unicode)
        print('%s, %s' % (glyph_unicode, glyph_name))

        if glyph_name and glyph_path:
            if glyph_name in name_mapper:
                glyph_name = name_mapper[glyph_name]
            icon_file = open(os.path.join('icons', glyph_unicode + '_' + glyph_name + '.svg'), 'w', encoding='UTF-8')
            icon_content = template.replace('{{ icon_path }}', glyph_path)
            icon_file.write(icon_content)
            icon_file.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))