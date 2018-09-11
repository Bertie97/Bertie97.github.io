#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import os, re, sys
import shutil, time
import markdown
import datetime as dt
import tkinter as tk
import numpy as np
from PIL import Image

DEBUG = False
eps = 0.0001
bkcolor = "white"
imgext = ['jpg', 'jpeg', 'bmp', 'png']

def lite(f, ext='_lite'):
    return os.extsep.join(f.split(os.extsep)[:-1]) + \
           ext + os.extsep + f.split(os.extsep)[-1]

def getlite(f, ext='_lite'):
    res = lite(f, ext)
    if os.path.exists(res): return res
    return f

def pagename(item):
    if not isinstance(item, dict) or 'timestamp' not in item: return ''
    return str(item['timestamp']).replace('.', '_') + '.html'

Dsample = 'SAMPLE'
for folder in ['js', 'css', 'res', 'img']:
    if DEBUG and os.path.exists(folder): shutil.rmtree(folder) # TODO: DELETE
    if not os.path.exists(folder):
        shutil.copytree(os.path.join(Dsample, folder), folder)
for file in os.listdir('pages'):
    os.remove(os.path.join('pages', file))

Fconfig = os.path.join('CONTENTS', 'CONFIG.md')
try:
    with open(Fconfig) as fp:
        lines = [l.strip() for l in fp.readlines()]
        validLines = [l for l in lines if l and not l.startswith('#')]
        locals().update({l.split('=')[0].strip(): eval('='.join(l.split('=')[1:]))
                         for l in validLines})
except FileNotFoundError: pass
defaults = {'MYNAME': "未命名", 'col': 4, 'row': 3, 'ratio': 0.64, 'entry': 10,
            'ccol': 3, 'giturl': ""}
for var in defaults:
    if var not in locals(): locals()[var] = defaults[var]
if 'foot' not in locals(): foot = "© " + MYNAME + " " + str(dt.datetime.now().year)

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
themes = {sec['foldername']: sec['theme'] for sec in sections}

def minifyPics(dir, size=300, ext='_lite'):
    for file in os.listdir(dir):
        parts = file.split(os.extsep)
        name, extension = os.extsep.join(parts[:-1]), parts[-1].lower()
        file = os.path.join(dir, file)
        if os.path.isdir(file):
            if themes.get(os.path.basename(file), '').upper() =='BLOG':
                minifyPics(file, size=750, ext='_lite')
                minifyPics(file, size=300, ext='_mini')
            else: minifyPics(file, size=size, ext=ext)
        if extension not in imgext: continue
        if '_lite' in file:
            if not os.path.exists(file.replace('_lite', '')):
                os.remove(file); continue
            lw, lh = Image.open(file).size
            w, h = Image.open(file.replace('_lite', '')).size
            if lw/lh - w/h < eps and lh == size: continue
            newfilename = file
            file = file.replace('_lite', '')
        elif '_mini' in file:
            if not os.path.exists(file.replace('_mini', '')):
                os.remove(file); continue
            lw, lh = Image.open(file).size
            w, h = Image.open(file.replace('_mini', '')).size
            if lw/lh - w/h < eps and lh == size: continue
            newfilename = file
            file = file.replace('_mini', '')
        else:
            newfilename = lite(file, ext)
            if os.path.exists(newfilename): continue
        image = Image.open(file)
        w, h = image.size
        try:
            int(name.split('-')[0])
            csize = 750
        except: csize = size
        w, h = w * csize // h, csize
        image = image.resize((w, h))
        image.save(open(newfilename, 'wb'))
minifyPics('CONTENTS')

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

header = '''
<div id="header" class="header">
    <div style="float:right; margin-top: 10px">
        <table>
            <tr>
                <td style="border: none; padding: 0;">
                    <a class="navitem" href="./index.html">首页</a>
                </td>
'''
for sec in sections:
    header += '''<td style="border: none; padding: 0;">
                     <a class="navitem" href="./{name}.html">{name}</a>
                 </td>'''.format(name=sec['name'])

header += '''
                <td style="border: none; padding: 0;">
                    <a class="navitem" href="./about.html">关于</a>
                </td>
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
        <h1 class="title"><span style="color:' + bkcolor + '"><b>{name}</b> 的主页</span></h1>
        <div style="width:100%; height:1rem"></div>
    </div>
</div>
'''.format(name=MYNAME)
footer = '<div id="footer"><a href="' + giturl
footer += '" style="text-decoration:none; color:white">' + foot + '</a></div>'
jquery = "js/jquery-3.3.1.min.js"
popout = '''
<div id='cover' style="z-index:1003; display:none"></div>
<div id="popout" style="z-index:1004; {astyle}; display:none"></div>
<div id="popcontent" style="display:none"><p>{}</p></div>
<ul class="pagination" id="cross" style="z-index:1005">
    <li id='closepop' style="display:none"><i class="mdi mdi-close-outline"></i></li>
</ul>
'''


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
                <a class="navitem" href="{name}.html">
                    <div class="block" style="height:{height}px">
                        <center>
                            <img class="round" src="{icon}"/>
                            <h4 style="margin:0">{name}</h4>
                            <p>{content}</p>
                        </center>
                    </div>
                </a>
            </td>
    '''.format(height=tk.Tk().winfo_screenheight() * 2 // 3, per=100 // len(sections),
               name=sec['name'], content=sec['text'], icon=getlite(sec['icon']))

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
    html = head(title=sec['title'].format(MYNAME), js=[jquery, "js/gallery.js"],
                css=["css/photos.css", 'res/css/materialdesignicons.min.css'])
    html += '<body onLoad="setPage(1,' + str(row) + ');" onkeydown="return onKey(event)">\n'
    html += '''
    <script type="text/javascript">
    function onKey(e)
    {
        var c = window.event ? event.keyCode : event.which;
        switch(c) {
            case 37: document.getElementById('page«').click(); break;
            case 39: document.getElementById('page»').click(); break;
        }
    }
    </script>
    '''
    html += header
    banner, gallery = [], []
    Dphotos = os.path.join('CONTENTS', sec['foldername'])
    for file in os.listdir(Dphotos):
        parts = file.split(os.extsep)
        name, extension = os.extsep.join(parts[:-1]), parts[-1].lower()
        if extension not in imgext: continue
        file = os.path.join(Dphotos, file)
        try: n = int(name.split('-')[0])
        except: n = None
        if n != None and n < 1000: banner.append(file)
        gallery.append((-os.stat(file).st_mtime, file))
    banner.sort()
    gallery.sort()
    gallery = [x[1] for x in gallery]
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
        			<a class="topop" href="javascript:;" name="{file}" target="_blank">
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
                        <a class="topop" href="javascript:;" name="{path}">
                            <img src="{litefile}" {con} style="border-radius:20px"/>
                        </a>
                    </center>
                </td>
        '''.format(path=f, con=constraint, litefile=getlite(f), per=100 // col)
        if i % col == col - 1: html += '\t\t</tr>\n'
        i += 1
    html += '</table>'
    numpages = i / (row * col)
    if numpages > int(numpages) + eps: numpages += 1
    numpages = int(numpages)
    if numpages > 1: html += pageButtons(numpages, row)
    pagetitle = sec['title'].format(MYNAME)
    html += footer
    html += popout.format('', astyle="opacity:0.5;")
    html += '<div class="wordsonpic" style="top:620px; width:{w}rem; margin-left:-{whf}rem; left: 50%;"><h1>'\
            .format(w=2*len(pagetitle), whf=len(pagetitle))
    html += pagetitle + '</h1></div>\n'
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
        if not item['content'].strip().startswith('#'):
            item['content'] = '#' + item['title'] + '\n' + item['content']
        buildMDPage(item, os.path.join(os.path.pardir, sec['name'] + '.html'), Dblogs,
                    prevurl=pagename(items[i-1] if i > 0 else None),
                    nexturl=pagename(items[i+1] if i < len(items) - 1 else None),
                    prturl=sec['name'] + '.html')
        info = time.localtime(item['timestamp'])
        Y, M, D = info.tm_year, info.tm_mon, info.tm_mday
        h, m, s = info.tm_hour, info.tm_min, info.tm_sec
        html += '''
            <tr>
                <td style="width:100%; border: none; padding: 0;">
                    <a href="{href}">
                        {hr}
                        <div class="tableitem">
                            <img style="background-image: url('{icon}')" class="blogIcon"/>
                            <h3>
                                {title}
                                <span id="timestamp">
                                    更新时间：{Y:04d}年{M:02d}月{D:02d}日{h:02d}时{m:02d}分{s:02d}秒
                                </span>
                            </h3>
                            <p id="intro">{subtitle}</p>
                        </div>
                    </a>
                </td>
            </tr>
        '''.format(href=os.path.join('pages', pagename(item)),
                   hr = '<hr>' if i % entry != 0 else '', icon=getlite(item['icon'], '_mini'),
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


def buildBOOK(sec):
    html = head(title=sec['title'].format(MYNAME), css=["css/book.css"], js=["js/book.js"])
    html += '<body onLoad="go2Page(1,' + str(entry) + ');">\n' + header
    books = []
    Dbooks = os.path.join('CONTENTS', sec['foldername'])
    DefaultIcon = None
    for dir in os.listdir(Dbooks):
        parts = dir.split(os.extsep)
        name, foldername = os.extsep.join(parts[:-1]), parts[-1]
        dir = os.path.join(Dbooks, dir)
        if name.upper() == 'DEFAULT' and extension in imgext:
            DefaultIcon = dir; continue
        if not os.path.isdir(dir): continue
        newbook = {'name': foldername, 'contents': [], 'intro': '', 'icon': None}
        ordered, unordered = [], []
        maxtimestamp = 0
        newest = None
        for file in os.listdir(dir):
            parts = file.split(os.extsep)
            name, extension = os.extsep.join(parts[:-1]), parts[-1].lower()
            file = os.path.join(dir, file)
            if name.upper() == 'ICON' and extension in imgext:
                newbook['icon'] = getlite(file, '_mini'); continue
            if extension != 'md': continue
            if name.lower().startswith('intro') or name.endswith('介绍'):
                with open(file) as fp: newbook['intro'] = fp.read()
                continue
            with open(file) as fp:
                chap = {'title': name, 'content': fp.read(), 'timestamp': os.stat(file).st_mtime}
            res = re.findall('[0-9]+', changeChineseNumToArab(name.split('_')[0]))
            if len(res) == 1: chap['chapter'] = res[0]; ordered.append(chap)
            else: unordered.append(chap)
            if chap['timestamp'] > maxtimestamp:
                maxtimestamp = chap['timestamp']
                newest = name
        ordered.sort(key=lambda c: c['chapter'])
        unordered.sort(key=lambda c: c['timestamp'])
        newbook['contents'] = unordered + ordered
        newbook['timestamp'] = maxtimestamp
        newbook['newest'] = newest
        if not newbook['intro'] and newbook['contents']:
            newbook['intro'] = newbook['contents'][0]['content'][:800]
        books.append(newbook)
    for book in books:
        if book['icon'] == None: book['icon'] = DefaultIcon
    books.sort(key=lambda x: -x['timestamp'])
    html += '''
    <div style="width:40rem; margin:auto">
        <center>
            <h1 id="main">{title}</h1>
            <hr style="background-image: url(res/hhr.png)">
        </center>
        <table id="blogList">
    '''.format(title=sec['title'].format(MYNAME))
    for i, book in enumerate(books):
        info = time.localtime(book['timestamp'])
        Y, M, D = info.tm_year, info.tm_mon, info.tm_mday
        h, m, s = info.tm_hour, info.tm_min, info.tm_sec
        html += '''
            <tr>
                <td style="width:100%">
                    <div class='row'>
                        <a href="{href}">
                            <img style="background-image: url('{icon}')" class="blogIcon"/>
                            <h3>
                                {title}
                                <span id="timestamp">
                                    更新时间：{Y:04d}年{M:02d}月{D:02d}日{h:02d}时{m:02d}分{s:02d}秒
                                </span>
                            </h3>
                            <p id="intro">{subtitle}</p>
                        </a>
                    </div>
                </td>
            </tr>
        '''.format(href=os.path.join('pages', book['name'] + '.html'),
                   hr = '<hr>' if i % entry != 0 else '', icon=book['icon'],
                   title = book['name'], Y=Y, M=M, D=D, h=h, m=m, s=s,
                   subtitle = book['intro'])
    html += '\t\t\t</table>\n'
    numpages = len(books) / entry
    if numpages > int(numpages) + eps: numpages += 1
    numpages = int(numpages)
    if numpages > 1: html += pageButtons(numpages, entry)
    html += '\t\t</div>\n'
    html += footer
    html += '</body>\n</html>'
    with open(sec['name'] + '.html', 'w') as fp: fp.write(html)
    # build the subpages
    for book in books:
        tinfo = time.localtime(book['timestamp'])
        Y, M, D = tinfo.tm_year, tinfo.tm_mon, tinfo.tm_mday
        h, m, s = tinfo.tm_hour, tinfo.tm_min, tinfo.tm_sec
        html = head(title=MYNAME + '的' + book['name'],
                    css=['../css/CHlist.css', '../res/css/materialdesignicons.min.css'],
                    js=['../' + jquery, '../js/book.js'])
        html += '<body>\n' + header.replace('"./', '"../')
        html += '''
        <div style="width:40rem; margin:auto">
            <ul class="pagination" style="float:left; margin:0.3rem; border-radius:0.1rem; width:1rem">
                <li><a href="''' + os.path.join(os.path.pardir, sec['name']) + '''.html">⬿</a></li>
            </ul>
            <div style="float:right; margin: 0.3rem; display:inline-block; padding:0; width:1rem"></div>
            <center><h1 id="main">{title}</h1></center>
            <div class='row'>
                <img style="background-image: url('{icon}')" class="mainIcon"/>
                <span id="timestamp" style="float:inherit">
                    最后更新：{newest}<br>{Y:04d}年{M:02d}月{D:02d}日{h:02d}时{m:02d}分{s:02d}秒
                </span>
                <a href="javascript:void(0)" style="text-decoration:none"><p id="intro">{intro}</p></a>
            </div>
            <div class='pod'>
                <center><h3>章节列表</h3></center>
                <table style="table-layout:fixed">
        '''.format(title=book['name'], icon=os.path.join(os.path.pardir, book['icon']),
                   intro=book['intro'], newest=book['newest'], Y=Y, M=M, D=D, h=h, m=m, s=s)
        for i, chap in enumerate(book['contents']):
            if not chap['content'].strip().startswith('#'):
                chap['content'] = '#' + chap['title'] + '\n' + chap['content']
            buildMDPage(chap, book['name'] + '.html', Dbooks,
                        prevurl=pagename(book['contents'][i-1] if i > 0 else None),
                        nexturl=pagename(book['contents'][i+1] if i < len(book['contents']) - 1 else None),
                        prturl=book['name'] + '.html')
            if i % ccol == 0: html += '\t\t\t\t\t<tr>\n'
            html += '''
                        <td>
                            <center><a href="{link}" class="chap">{title}</a></center>
                        </td>
            '''.format(title=chap['title'], link=pagename(chap))
            if i % ccol == ccol - 1: html += '\t\t\t\t\t</tr>\n'
        html += '\t\t\t\t</table>\n\t\t\t</div>\t\t</div>\n'
        html += footer
        html += popout.format(book['intro'], astyle="")
        html += '</body>\n</html>'
        with open(os.path.join('pages', book['name'] + '.html'), 'w') as fp: fp.write(html)


def buildMDPage(item, parenturl, dir, prevurl='', nexturl='', prturl=''):
    html = head(title=item['title'], css=['../css/blog.css'], js=['../' + jquery, '../js/blog.js'])
    # html += '<body>\n' + header.replace('./', '../')
    shiftable = prevurl or nexturl or prturl
    html += '<body' + (' onkeydown="return onKey(event)"' if shiftable else '') + '>\n'
    if shiftable:
        html += '''
        <script type="text/javascript">
        function onKey(e)
        {
            var c = window.event ? event.keyCode : event.which;
            switch(c) {
                case 8:  document.getElementById('back').click(); break;
                case 13: document.getElementById('list').click(); break;
                case 37: document.getElementById('prev').click(); break;
                case 39: document.getElementById('next').click(); break;
            }
        }
        </script>
        '''
    html += header.replace('./', '../')
    html += '\t<div style="width:40rem; margin:2rem auto; padding:6rem;\
    box-shadow: 2px 2px 4px #888; border-radius:0.4rem;" id="page">\n'
    change = []
    tmp = item['content']
    start = 0
    while True:
        res = re.search(r'!\[[^\[\]]*\]\(', tmp)
        if res == None: break
        remove = False
        p = res.span()[0] - 1
        while p >= 0 and tmp[p] in [' ', '\t']: p -= 1
        if p >= 0 and tmp[p] == '#': imgstart = p; remove = True
        lindx = res.span()[1]
        rindx = tmp.find(')', lindx)
        path = tmp[lindx:rindx]
        if not os.path.isabs(path) and not os.path.exists(path) and '://' not in path:
            path = os.path.join(os.path.pardir, dir, '') + path
        path = getlite(path)
        if remove: change.append((imgstart + start, rindx + start + 1, ''))
        else: change.append((lindx + start, rindx + start, path))
        tmp = tmp[rindx:]
        start += rindx
    md = item['content']
    for l, r, s in change[::-1]: md = md[:l] + s + md[r:]
    for i in range(len(md)-1, 0, -1):
        if md[i] != '\n': continue
        if md[i-1] == '\n': continue
        if i < len(md) - 1 and md[i+1] == '\n': continue
        try:
            ind = md.rindex('\n', 0, i)
        except ValueError: ind = 0
        if md[ind:i].strip().startswith('#'):
            md = md[:i] + '\n' + md[i:]; continue
        md = md[:i] + '<br>' + md[i+1:]
    html += '''
    <ul class="pagination">
        <li><a href="''' + parenturl + '''" id="back">⬿</a></li>
    </ul>
    '''
    html += markdown.markdown(md)
    if shiftable:
        html += '''
        <center>
            <ul class="pagination">
        '''
        if prevurl: html += '<li><a href="' + prevurl + '" id="prev">«</a></li>\n'
        else: html += '<li><a id="prev" style="color:' + bkcolor + '">«</a></li>\n'
        if prturl: html += '<li><a href="' + prturl + '" id="list">≡</a></li>\n'
        else: html += '<li><a id="list" style="color:' + bkcolor + '">≡</a></li>\n'
        if nexturl: html += '<li><a href="' + nexturl + '" id="next">»</a></li>\n'
        else: html += '<li><a id="next" style="color:' + bkcolor + '">»</a></li>\n'
        html += '''
            </ul>
        </center>
        '''
    html += '\t</div>\n'
    html += '<center><img src="../img/arrowUP.png" id="goToTop" name="goToTop"/></center>\n'
    html += footer + '</body>\n</html>'
    if not os.path.exists('pages') or not os.path.isdir('pages'): os.mkdir('pages')
    with open(os.path.join('pages', pagename(item)), 'w') as fp: fp.write(html)


def chinese2digits(uchars_chinese):
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(uchars_chinese) - 1, -1, -1):
        val = {'序': 0, '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5,
               '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '百': 100, '千': 1000,
               '万': 10000, '亿': 100000000}.get(uchars_chinese[i])
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
                # total =total + r * x
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
    return total


num_str_start_symbol = ['序', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九',
                        '十']
more_num_str_symbol = ['序', '零', '一', '二', '两', '三', '四', '五', '六', '七', '八',
                       '九', '十', '百', '千', '万', '亿']

def changeChineseNumToArab(oriStr):
    lenStr = len(oriStr);
    aProStr = ''
    if lenStr == 0:
        return aProStr;

    hasNumStart = False;
    numberStr = ''
    for idx in range(lenStr):
        if oriStr[idx] in num_str_start_symbol:
            if not hasNumStart:
                hasNumStart = True;

            numberStr += oriStr[idx]
        else:
            if hasNumStart:
                if oriStr[idx] in more_num_str_symbol:
                    numberStr += oriStr[idx]
                    continue
                else:
                    numResult = str(chinese2digits(numberStr))
                    numberStr = ''
                    hasNumStart = False;
                    aProStr += numResult

            aProStr += oriStr[idx]
            pass

    if len(numberStr) > 0:
        resultNum = chinese2digits(numberStr)
        aProStr += str(resultNum)

    return aProStr


for sec in sections:
    theme = sec['theme'].upper()
    if theme not in ['GALLERY', 'BLOG', 'BOOK']:
        raise TypeError("Unrecognized theme " + theme+ '.')
    exec('build' + theme + '(sec)')

time.sleep(1)
os.system("open index.html")
