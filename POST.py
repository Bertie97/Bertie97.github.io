#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import os, re, sys, shutil, time, markdown
import tkinter as tk
import numpy as np
from PIL import Image

eps = 0.0001
imgext = ['jpg', 'jpeg', 'bmp', 'png']

lite = lambda f: os.extsep.join(f.split(os.extsep)[:-1]) + \
                 '_lite' + os.extsep + f.split(os.extsep)[-1]

def minifyPics(dir):
    for file in os.listdir(dir):
        file = os.path.join(dir, file)
        if os.path.isdir(file): minifyPics(file)
        if file.split(os.extsep)[-1].lower() not in imgext: continue
        if '_lite' in file: continue
        newfilename = lite(file)
        if os.path.exists(newfilename): continue
        image = Image.open(file)
        w, h = image.size
        w, h = w * 300 // h, 300
        image = image.resize((w, h))
        image.save(open(newfilename, 'wb'))
minifyPics('CONTENTS')

Fconfig = os.path.join('CONTENTS', 'CONFIG.md')
with open(Fconfig) as fp:
    lines = [l.strip() for l in fp.readlines()]
    validLines = [l for l in lines if l and not l.startswith('#')]
    locals().update({l.split('=')[0].strip(): eval('='.join(l.split('=')[1:]))
                     for l in validLines})

def head(title='', js=[], css=[], other=''):
    s = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>{title}</title>
'''.format(title=title)
    for f in js: s += '<script type="text/javascript" src="' + f + '"></script>\n'
    for f in css: s += '<link type="text/css" rel="stylesheet" href="' + f + '"/>\n'
    s += other
    s += '</head>\n'
    return s

Dsample = 'SAMPLE'
for folder in ['js', 'css', 'res', 'img']:
    if not os.path.exists(folder):
        shutil.copytree(os.path.join(Dsample, folder), folder)

Dabout = os.path.join('CONTENTS', 'ABOUT')
intro = ''; sections = []
for file in os.listdir(Dabout):
    parts = file.split(os.extsep)
    name, extension = os.extsep.join(parts[:-1]), parts[-1].lower()
    if name.lower() == 'main':
        with open(os.path.join(Dabout, file)) as fp:
            intro = fp.read()
        continue
    if extension != 'md': continue
    tag = ''
    if '-' in name: tag = name.split('-')[0]; name = name[name.index('-')+1:]
    with open(os.path.join(Dabout, file)) as fp:
        content = fp.read()
    info = []
    icon = ''
    fname = name
    theme = 'BLOG'
    title = '{}的主页'
    for line in content.split('\n'):
        if not line.strip(): continue
        if line.startswith('!'):
            a, b = re.search(r'\[.*\]', line).span()
            c, d = re.search(r'\(.*\)', line).span()
            fname = line[a+1:b-1]
            icon = line[c+1:d-1]
            if not os.path.isabs(icon) and not os.path.exists(icon) and '://' not in icon:
                icon = os.path.join(Dabout, icon)
            continue
        if line.startswith('Theme:'):
            theme = line[6:].strip()
            continue
        if line.startswith('Title:'):
            title = line[6:].strip()
            continue
        info.append(line)
    sections.append({'foldername': fname, 'name': name, 'icon': icon, 'title':title,
                   'tag': tag, 'text': '\n'.join(info), 'theme': theme})
sections = sorted(sections, key=lambda x: x['tag'])

header = '''
<div id="header" class="header">
    <div style="float:right; margin-top: 10px">
        <table>
            <tr>
                <td><a class="navitem" href="./index.html">首页</a></td>
'''
for sec in sections:
    header += '<td><a class="navitem" href="./{name}.html">{name}</a></td>'.format(name=sec['name'])

header += '''
                <td><a class="navitem" href="./about.html">关于</a></td>
            </tr>
        </table>
    </div>
    <div id="title">
        <h1 class="title"><b>{name}</b> 的网页</h1>
        <hr style="width:100%; margin:0">
    </div>
</div>
<div class="header" style="border:none">
    <div id="title">
        <h1 class="title"><span style="color:white"><b>{name}</b> 的主页</span></h1>
        <div style="width:100%; height:1rem"></div>
    </div>
</div>
'''.format(name=MYNAME)
footer = '<div id="footer">© BFG Bertie 2018</div>'
jquery = "js/jquery-3.3.1.min.js"


# build index.html
################################################################################
html = head(title=MYNAME+"的主页", js=[jquery, "js/main.js"], css=["css/main.css"])
html += '<body>\n'
html += header
html += '<img id="mainpic" src="' + os.path.join('CONTENTS', 'MAIN_lite.JPG') + '" width="100%" height="100%"/>\n'
html += '''
<div width="100%">
    <center><h1 style="color:cornflowerblue;">板块</h1></center>
    <table>
        <tr>
'''
about = ''
for sec in sections:
    about += '''
            <td width="{per}%">
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
    '''.format(height=tk.Tk().winfo_screenheight() * 2 // 3, per=100 // len(sections),
               name=sec['name'], content=sec['text'], icon=lite(sec['icon']))

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
html = head(title=MYNAME+"的网页介绍", js=["js/main.js"], css=["css/about.css"])
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


def pageButtons(npages, nrows):
    res = '''
    <center>
        <ul class="pagination">
            <li><a id="page«" onclick="movePage(-1, {s});">«</a></li>
    '''.format(s=nrows)
    for i in range(npages):
        res += '\t\t\t<li><a id="page{n}" onclick="go2Page({n}, {row});">{n}</a></li>'.format(n=i+1, row=nrows)
    return res + '''
            <li><a id="page»" onclick="movePage(+1, {s});">»</a></li>
        </ul>
    </center>
    '''.format(s=nrows)


def buildGALLERY(sec):
    html = head(title=sec['title'].format(MYNAME), css=["css/photos.css"])
    html += '<body onLoad="setPage(1,' + str(row) + ');">\n' + header
    banner, gallery = [], []
    Dphotos = os.path.join('CONTENTS', sec['foldername'])
    for file in os.listdir(Dphotos):
        parts = file.split(os.extsep)
        name, extension = os.extsep.join(parts[:-1]), parts[-1].lower()
        if extension not in imgext: continue
        try: n = int(name)
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
        <script type="text/javascript" src="{jq}"></script>
        <script type="text/javascript" src="js/photos.js"></script>
        '''.format(jq=jquery)
    html += '''
        <table id="gallery">
            '''
    i = 0
    for f in gallery:
        if '_lite' in f: continue
        if i % col == 0: html += '\t\t<tr>\n'
        w, h = Image.open(f).size; p = 95
        if ratio * w < h: constraint = 'width="{per}%"'.format(per=int(p*ratio*w/h))
        else: constraint = 'width="{per}%"'.format(per=p)
        html += '''
                <td width="{per}%">
                    <center>
                        <a href="{path}">
                            <img src="{litefile}" {con} style="border-radius:20px"/>
                        </a>
                    </center>
                </td>
        '''.format(path=f, con=constraint, litefile=lite(f), per=100 // col)
        if i % col == col - 1: html += '\t\t</tr>\n'
        i += 1
    html += '</table>'
    numpages = i / (row * col)
    if numpages > int(numpages) + eps: numpages += 1
    numpages = int(numpages)
    if numpages > 1: html += pageButtons(numpages, row)
    html += footer
    html += '<div class="wordsonpic" style="top:620px"><h1>'
    html += sec['title'].format(MYNAME) + '</h1></div>\n'
    html += '<div id="GLY" name="GLY" style="position:absolute; top:640px"/>\n'
    html += '</body>\n</html>'
    with open(sec['name'] + '.html', 'w') as fp: fp.write(html)


def buildBLOG(sec):
    html = head(title=sec['title'].format(MYNAME), css=["css/blog.css"], js=["js/blog.js"])
    html += '<body onLoad="go2Page(1,' + str(entry) + ');">\n' + header
    items = []
    Dblogs = os.path.join('CONTENTS', sec['foldername'])
    DefaultIcon = None
    for file in os.listdir(Dblogs):
        parts = file.split(os.extsep)
        name, extension = os.extsep.join(parts[:-1]), parts[-1].lower()
        file = os.path.join(Dblogs, file)
        if name.upper() == 'DEFAULT' and extension in imgext:
            DefaultIcon = file; continue
        if extension != 'md': continue
        with open(file) as fp: content = fp.read()
        newitem = {}
        newitem['timestamp'] = os.stat(file).st_mtime
        newitem['title'] = name
        newitem['content'] = content
        newitem['subtitle'] = re.sub(r'!\[[^\[\]]*\]\([^\(\)]+\)', '[图片]', content)[:1000].replace('#', '').replace('**', '').replace('`', '')
        index = content.find('![COVER](')
        if index < 0: index = content.find('![LAUNCHER](')
        if index < 0: newitem['icon'] = None
        else:
            ridx = content.find(')', index + 9)
            path = content[index + 9: ridx]
            if not os.path.isabs(path) and not os.path.exists(path) and '://' not in path:
                path = os.path.join(Dblogs, path)
            newitem['icon'] = path
        items.append(newitem)
    for item in items:
        if item['icon'] == None: item['icon'] = DefaultIcon
    items.sort(key=lambda x: -x['timestamp'])
    html += '''
    <div style="width:40rem; margin:auto">
        <center>
            <h1 id="main">{title}</h1>
            <hr style="background-image: url(res/hhr.png)">
        </center>
        <table id="blogList">
    '''.format(title=sec['title'].format(MYNAME))
    for i, item in enumerate(items):
        buildMDPage(item, Dblogs)
        info = time.localtime(item['timestamp'])
        Y, M, D = info.tm_year, info.tm_mon, info.tm_mday
        h, m, s = info.tm_hour, info.tm_min, info.tm_sec
        html += '''
            <tr>
                <td style="width:100%">
                    <a href="{href}">
                        {hr}
                        <img style="background-image: url('{icon}')" class="blogIcon"/>
                        <h3>
                            {title}
                            <span id="timestamp">
                                更新时间：{Y:04d}年{M:02d}月{D:02d}日{h:02d}时{m:02d}分{s:02d}秒
                            </span>
                        </h3>
                        <p id="intro">{subtitle}</p>
                    </a>
                </td>
            </tr>
        '''.format(href=os.path.join('pages', str(item['timestamp']).replace('.', '_') + '.html'),
                   hr = '<hr>' if i % entry != 0 else '', icon=lite(item['icon']),
                   title = item['title'], Y=Y, M=M, D=D, h=h, m=m, s=s,
                   subtitle = item['subtitle'])
    html += '\t\t\t</table>\n'
    numpages = len(items) / entry
    if numpages > int(numpages) + eps: numpages += 1
    numpages = int(numpages)
    if numpages > 1: html += pageButtons(numpages, entry)
    html += '\t\t</div>\n'
    html += footer
    html += '</body>\n</html>'
    with open(sec['name'] + '.html', 'w') as fp: fp.write(html)

def buildMDPage(item, dir):
    html = head(title=item['title'], css=['../css/blog.css'], js=['../' + jquery, '../js/blog.js'])
    html += '<body>\n' + header.replace('./', '../')
    html += '\t<div style="width:40rem; margin:auto">\n'
    insert = []
    tmp = item['content']
    start = 0
    while True:
        res = re.search(r'!\[[^\[\]]*\]\(', tmp)
        if res == None: break
        lindx = res.span()[1]
        rindx = tmp.find(')', lindx)
        path = tmp[lindx:rindx]
        if not os.path.isabs(path) and not os.path.exists(path) and '://' not in path:
            insert.append(lindx + start)
        tmp = tmp[rindx:]
        start += rindx
    parts = []; s = 0
    for i in insert: parts.append(item['content'][s:i]); s = i
    parts.append(item['content'][s:])
    md = (os.path.join(os.path.pardir, dir, '')).join(parts)
    html += markdown.markdown(md)
    html += '\t</div>\n'
    html += '<center><img src="../img/arrowUP.png" id="goToTop" name="goToTop"/></center>\n'
    html += footer + '</body>\n</html>'
    if not os.path.exists('pages') or not os.path.isdir('pages'): os.mkdir('pages')
    with open(os.path.join('pages', str(item['timestamp']).replace('.', '_') + '.html'), 'w') as fp: fp.write(html)

for sec in sections:
    if sec['theme'].upper() == 'GALLERY': buildGALLERY(sec)
    if sec['theme'].upper() == 'BLOG': buildBLOG(sec)
