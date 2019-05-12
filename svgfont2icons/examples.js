var fs = require('fs')
var file = fs.readFileSync('./iconfont.css', 'utf8').toString();
var os = require('os')
 
var icons = file.split('\n');
var getColor = function () {
    return '#' + Math.random().toString(16).substr(-6);
}
var html = '<!DOCTYPE html>' +
    '<html lang="en">' +
    '<head>' +
    '    <meta charset="UTF-8">' +
    '    <title>iconfont查看</title>' +
    '<link rel="stylesheet" href="./iconfont.css">' +
    '<style>.iconfont{font-size: 44px;height: 44px;width: 44px;margin: 4px;}</style>' +
    '</head>' +
    '<body>';

html += '<p>总数：' + icons.length + '</p>\n';

for (var i = 0; i < icons.length; i++) {
    var icon = icons[i];
    if (icon.includes('icon-')) {
        var className = icon.split('.')[1].split(':')[0];
        var unicode = icon.split('.')[1].split(':')[2].split('"')[1].replace('\\', '');
        html += '<div style="display:inline-block;"><i class="iconfont ' + className + '"></i><div>' + className + '</div><div>' + unicode + '</div></div>\n';
    }
}
html += '<script>\n' +
    '    var getColor = function () {\n' +
    '        return \'#\' + Math.random().toString(16).substr(-6);\n' +
    '    }\n' +
    '    var icons = document.getElementsByTagName(\'i\')\n' +
    '    for (var i = 0; i < icons.length; i++) {\n' +
    '        var icon = icons[i];\n' +
    '        icon.style.color = getColor()\n' +
    '    }\n' +
    '</script></body>' +
    '</html>'
 
fs.writeFileSync('./examples.html', html)
