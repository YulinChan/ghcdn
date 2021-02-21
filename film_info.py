#!/usr/bin/python3
import os
import re
import time

import requests
from pprint import pprint
from bs4 import BeautifulSoup



def film_info(url):
    hd = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}
    r = requests.get(url, headers=hd)
    soup = BeautifulSoup(r.text, 'lxml')
    soup.prettify()
    title = soup.find('h1', {'class': "ts"}).text.replace('\n', '')
    print("开始处理", title)
    article_content = soup.find('div', {'id': re.compile(r"post_\d*?")}).find('div', {
        'class': "t_fsz"}).table.find('td')
    article_img = article_content.find_all('img')
    img = []
    for j in article_img:
        if 'http' in j['file']:
            img.append(j['file'])
        else:
            img.append('https://www.sehuatang.net/' + j['file'])
    print(img)
    print("封面图片提取完毕！")

    bt = soup.find('div', {'id': re.compile(r"post_\d*?")}).find('div', {'class': "t_fsz"}).find('p', {
        'class': "attnm"})
    name = bt.text.strip().replace('.torrent','')
    torrent = 'https://www.sehuatang.net/' + bt.a['href']
    print(name, torrent)
    print("种子信息提取完毕！")

    # 下载封面图片
    for i,url in zip(range(len(img)),img):
        res = requests.get(url, headers=hd)
        with open(f'pic{i}.jpg','wb') as pic:
            pic.write(res.content)
    print("封面图片已下载！")

    # 生成影片信息
    with open('README.md','a+') as md:
        md.write('## '+f"[{title}](https://cdn.jsdelivr.net/gh/ghcdn/{name}/res/index.m3u8)"+'\n')
        for i in range(len(img)):
            md.write(f"![](./pic{i}.jpg)\n")
    with open('index.html', 'w+') as html:
        s = html.read()
        h5 = s.replace("{name}", name).replace("{title}",title)
        html.write(h5)
    print("影片信息已生成！")

    # 生成下载信息
    with open('name.txt','w') as n:
        n.write(name)
    with open('url.txt','w') as dlink:
        dlink.write(torrent)
    print("影片信息已生成！")
    print(title, "处理完毕！")

def add_tracker(url):
    r = requests.get(url)
    trackers = r.text.splitlines()
    tracker_list = []
    for i in trackers:
        if i:
            tracker_list.append(i)
    with open('aria2.conf', 'a+') as conf:
        conf.write(f"bt-tracker={tracker_list}")
    pprint(tracker_list)
    print("tracker添加完毕！")

if __name__ == '__main__':
    with open('task.txt', 'r') as f:
      link = f.read()
      film_info(link)
    tracker_url = "https://ngosang.github.io/trackerslist/trackers_best.txt"
    add_tracker(tracker_url)

