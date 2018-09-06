#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import os, re, sys, shutil
import tkinter as tk
import numpy as np
from PIL import Image

imgext = ['jpg', 'jpeg', 'bmp', 'png']

def minifyPics(dir):
    for file in os.listdir(dir):
        file = os.path.join(dir, file)
        if os.path.isdir(file): minifyPics(file)
        nameparts = file.split(os.extsep)
        if nameparts[-1].lower() not in imgext: continue
        if '_lite' in file: continue
        newfilename = os.extsep.join(nameparts[:-1]) + '_lite' + os.extsep + nameparts[-1]
        if os.path.exists(newfilename): continue
        image = Image.open(file)
        w, h = image.size
        w, h = w * 480 // h, 480
        image = image.resize((w, h))
        image.save(open(newfilename, 'w'))
minifyPics('CONTENTS')

Fconfig = os.path.join('CONTENTS', 'CONFIG.md')
with open(Fconfig) as fp:
    lines = [l.strip() for l in fp.readlines()]
    validLines = [l for l in lines if l and not l.startswith('#')]
    locals().update({l.split('=')[0].strip(): eval('='.join(l.split('=')[1:]))
                     for l in validLines})

def head(title='', js=[], css=[]):
    s = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>{title}</title>
'''.format(title=title)
    for f in js: s += '<script type="text/javascript" src="' + f + '"></script>\n'
    for f in css: s += '<link type="text/css" rel="stylesheet" href="' + f + '"/>\n'
    s += '</head>\n'
    return s

Dsample = 'SAMPLE'
for folder in ['js', 'css', 'res', 'img']:
    if not os.path.exists(folder):
        shutil.copytree(os.path.join(Dsample, folder), folder)

Dabout = os.path.join('CONTENTS', 'ABOUT')
intro = ''; boards = {}
for file in os.listdir(Dabout):
    parts = file.split(os.extsep)
    if len(parts) != 2: continue
    name, extension = parts
    if name.lower() == 'main':
        with open(os.path.join(Dabout, file)) as fp:
            intro = fp.read()
        continue
    if extension.lower() != 'md': continue
    tag = ''
    if '-' in name: tag = name.split('-')[0]; name = name[name.index('-')+1:]
    with open(os.path.join(Dabout, file)) as fp:
        content = fp.read()
    icon = ''
    if content.startswith('!'):
        a, b = re.search(r'\[.*\]', content).span()
        c, d = re.search(r'\(.*\)', content).span()
        name = content[a+1:b-1]
        icon = content[c+1:d-1]
        if not os.path.isabs(icon): icon = os.path.join(Dabout, icon)
        content = content[d+1:].strip()
    boards[name] = {'icon': icon, 'tag': tag, 'text': content}
boards = dict(sorted(boards.items(), key=lambda x: x[1]['tag']))
for key in boards: boards[key].pop('tag')

header = '''
<div id="header" class="header">
    <div style="float:right; margin-top: 10px">
        <table>
            <tr>
                <td><a class="navitem" href="index.html">首页</a></td>
'''
for key in boards:
    header += '<td><a class="navitem" href="{name}.html">{name}</a></td>'.format(name=key)

header += '''
                <td><a class="navitem" href="about.html">关于</a></td>
            </tr>
        </table>
    </div>
    <div id="title">
        <h1 class="title"><b>{name}</b> 的主页</h1>
        <hr style="width:100%; margin:0">
    </div>
</div>
<div class="header" style="border:none"><div id="title">
    <h1 class="title"><span style="color:white"><b>{name}</b> 的主页</span></h1>
    <div style="width:100%; height:1rem">
</div></div>
'''.format(name=MYNAME)
footer = '<div id="footer">© BFG Bertie 2018</div>'


# build index.html
################################################################################
html = head(title=MYNAME+"的主页", js=["js/jquery-3.3.1.min.js", "js/main.js"], css=["css/main.css"])
html += '<body>\n'
html += header
html += '<img id="mainpic" src="./img/MAIN.JPG" width="100%" height="100%"/>\n'
html += '''
<div width="100%">
    <center><h1 style="color:cornflowerblue;">板块</h1></center>
    <table style="table-layout:fixed">
        <tr>
'''
about = ''
for key in boards:
    about += '''
            <td>
                <div class="block" style="height:{height}px">
                    <center>
                        <a class="navitem" href="{name}.html">
                            <img class="round" src="{icon}"/>
                            <h4 style="margin:0">{name}</h4>
                            <p>{content}</p>
                        </a>
                    </center>
                </div>
            </td>
    '''.format(height=tk.Tk().winfo_screenheight() * 2 // 3,
               name=key, content=boards[key]['text'], icon=boards[key]['icon'])

html += about + '''
        </tr>
    </table>
</div>
'''
html += footer
html += '''
<div class="wordsonpic">
    <h1>欢迎来到{name}的主页</h1>
    <p style="font-size:0.8rem; margin:0.4rem">点击下方按钮或滚动了解更多</p>
    <button id="mainbutton" type="button"; style="margin:20px">介绍</button>
</div>
<center>
    <img src="./img/arrowUP.png" height="5%" id="arrowUP"/>
</center>
'''.format(name=MYNAME)
html += '</body>\n</html>'
with open('index.html', 'w') as fp: fp.write(html)

# build about.html
html = head(title=MYNAME+"主页的介绍", js=["js/main.js"], css=["css/about.css"])
html += '<body>\n' + header
html += '''
<div width="100%">
    <h1 id="main">介绍</h1>
    <p style="margin-left:4rem">''' + intro + '''</p>
    <table style="table-layout:fixed">
        <tr>
'''
html += about + '''
        </tr>
    </table>
</div>
'''
html += footer + '</body>\n</html>'
with open('about.html', 'w') as fp: fp.write(html)

# build photos
################################################################################
html = head(title=MYNAME+"的摄影作品", css=["css/photos.css"])
html += '<body>\n' + header
banner, gallery = [], []
Dphotos = os.path.join('CONTENTS', 'PHOTOS')
for file in os.listdir(Dphotos):
    if file.split(os.extsep)[-1].lower() not in imgext: continue
    try: n = int(file.split(os.extsep)[0])
    except: n = None
    if n != None and n < 1000: banner.append(os.path.join(Dphotos, file))
    gallery.append(os.path.join(Dphotos, file))
banner.sort()
gallery.sort()
if banner:
    html += '''
    <div class="slide-main" id="touchMain">
    	<a class="prev" href="javascript:;" stat="prev1001"><img src="img/l-btn.png" /></a>
    	<div class="slide-box" id="slideContent">
        '''
    with open(os.path.join(Dphotos, 'picInfo.md')) as fp: lines = fp.readlines()
    lines = [x.strip() for x in lines]
    parts = [x.split() for x in lines if x]
    chex = lambda x: '{:^03}'.format(hex(x)[2:])[:2]
    cmap = {x[0]: [int(u) for u in x[1:]] for x in parts}
    for f in banner:
        if f in cmap: r, g, b, w, h = cmap[f]
        else:
            image = Image.open(f)
            data = np.array(image)
            r, g, b = np.mean(data[:,:,0]), np.mean(data[:,:,1]), np.mean(data[:,:,2])
            r, g, b = int(r), int(g), int(b)
            w, h = image.size
            cmap[f] = r, g, b, w, h
        w = w * 640 // h
        html += '''
    		<div class="slide" style="background-color:rgb({r},{g},{b})">
    			<a href="{file}" target="_blank">
    				<div class="obj" style="left:50%; margin-left:-{hfw}px; width:{w}px" >
                        <img src="{file}" class='pic'/>
                    </div>
    			</a>
    		</div>
            '''.format(r=r, g=g, b=b, file=f, w=w, hfw=w//2)
    with open(os.path.join(Dphotos, 'picInfo.md'), 'w') as fp:
        fp.write('\n'.join([' '.join([im] + [str(t) for t in cmap[im]]) for im in cmap]))
    html += '''
    	</div>
    	<a class="next" href="javascript:;" stat="next1002"><img src="img/r-btn.png" /></a>
    	<div class="item">
    		<a class="cur" stat="item1001" href="javascript:;"></a>
            '''
    for k in range(len(banner) - 1):
        html += '<a href="javascript:;" stat="item1%03d"></a>'%(k+2,)
    html += '''
    	</div>
    </div>
    '''
    html += '''
    <script type="text/javascript" src="js/jquery-3.3.1.min.js"></script>
    <script type="text/javascript" src="js/photos.js"></script>
    '''
html += '''
    <table style="table-layout:fixed" cellpadding="20px">
        <tr>
        '''
i = 0
for f in gallery:
    if '_lite' in f: continue
    w, h = Image.open(f).size; p = 95
    if ratio * w < h: constraint = 'width="{per}%"'.format(per=int(p*ratio*w/h))
    else: constraint = 'width="{per}%"'.format(per=p)
    html += '''
            <td>
                <center>
                    <a href="{path}">
                        <img src="{litefile}" {con} style="border-radius:20px"/>
                    </a>
                </center>
            </td>
    '''.format(path=f, con=constraint,
               litefile=os.extsep.join(f.split(os.extsep)[:-1]) +
                        '_lite' + os.extsep + f.split(os.extsep)[-1])
    if i % col == col - 1: html += '\t\t</tr>\n\t\t<tr>'
    i += 1
html += '''
        </tr>
    </table>
'''
html += footer
html += '<div class="wordsonpic" style="top:620px"><h1>摄影作品</h1></div>\n'
html += '</body>\n</html>'
with open('摄影.html', 'w') as fp: fp.write(html)
