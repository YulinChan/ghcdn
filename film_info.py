#!/usr/bin/python3
import os
import re
import time

import requests
from bs4 import BeautifulSoup



def film_info(url):
    hd = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}
    r = requests.get(url, headers=hd)
    soup = BeautifulSoup(r.text, 'lxml')
    soup.prettify()
    title = soup.find('h1', {'class': "ts"}).text.replace('\n', '')
    article_content = soup.find('div', {'id': re.compile(r"post_\d*?")}).find('div', {
        'class': "t_fsz"}).table.find('td')
    article_img = article_content.find_all('img')
    img = []
    for j in article_img:
        if 'http' in j['file']:
            img.append(j['file'])
        else:
            img.append('https://www.sehuatang.net/' + j['file'])

    bt = soup.find('div', {'id': re.compile(r"post_\d*?")}).find('div', {'class': "t_fsz"}).find('p', {
        'class': "attnm"})
    name = bt.text.strip().split('.')[0]
    torrent = 'https://www.sehuatang.net/' + bt.a['href']
    # 下载封面图片
    for i,url in zip(range(len(img)),img):
    	res = requests.get(url, headers=hd)
    	with open(f'pic{i}.jpg','wb') as pic:
    		pic.write(res.content)
    # 生成影片信息
    with open('README.md','a+') as md:
    	md.write('## '+f"[{title}](https://cdn.jsdelivr.net/gh/ghcdn{name}/res/index.m3u8)"+'\n')
    	for i in range(len(img)):
    		md.write(f"![](./pic{i}.jpg)\n")
    # 生成下载信息
    with open('name.txt','w') as n:
    	n.write(name)
    with open('url.txt','w') as dlink:
    	dlink.write(torrent)
    print(title, "done !")

if __name__ == '__main__':
	with open('index.txt', 'r') as f:
		link = f.read()
		film_info(link)