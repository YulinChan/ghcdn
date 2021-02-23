#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}


def setup():
    # 解析任务
    task = open('task.txt', 'r')
    url = open('url.txt', 'w')
    video = open('video.txt', 'w')
    repo = open('repo.txt', 'w')
    info = task.read().splitlines()
    url.write(info[0])
    video.write(info[1])
    repo.write(info[2])
    task.close()
    url.close()
    repo.close()
    print(info[0], info[1], info[2], "任务解析完毕！")
    return info[2]


def gen_film_info(video_id):
    try:
        r = requests.get(f'https://www.javbus.com/{video_id}', headers=header)
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.find('h3').text.strip()
        poster = soup.find('div', {'class': 'screencap'}).a['href']
        info = soup.find('div', {'class': 'info'}).text.strip()
        img = soup.find('div', id='sample-waterfall').find_all('a')
        img_links = [poster]
        for i in img:
            img_links.append(i['href'])

        for i, url in zip(range(len(img_links)), img_links):
            r = requests.get(url, headers=header)
            with open(f"pic{i}.jpg", 'wb') as pic:
                pic.write(r.content)
        print(info)
        print(img_links)
        print(title, "信息提取完毕！")
    except Exception as e:
        title = video_id
        info = ''
        img_links = []
        print(e, "没找到相关影片信息！")

    # 生成影片信息
    hls = open('hls.html', 'r')
    html = open('index.html', 'w')
    html.write(hls.read().replace(
        '{repo}', video_id).replace('{title}', title))
    hls.close()
    html.close()
    md = open('README.md', 'a+')
    md.write(
        f'## [{title}](https://cdn.jsdelivr.net/gh/ghcdn/{video_id}/res/index.m3u8)\n\n')
    md.write(info+'\n\n')
    for i in range(len(img_links)):
        md.write(f"![](./pic{i}.jpg)\n")
    for i in range(6):
        md.write(f"![](./thumb0{i+1}.jpg)\n")
    print("影片信息已生成！")


def add_tracker(url):
    r = requests.get(url)
    trackers = r.text
    conf = open('aria2.conf', 'a+')
    conf.write(f'bt-tracker={trackers}')
    conf.close()
    with open('aria2.conf', 'r') as f:
        print(f.read())
    print("tracker添加完毕！")


if __name__ == '__main__':
    vid = setup()
    try:
        gen_film_info(vid)
    except Exception as e:
        print(e)
    tracker_url = "https://trackerslist.com/best_aria2.txt"
    add_tracker(tracker_url)
