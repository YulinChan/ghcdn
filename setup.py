#!/usr/bin/python3
import requests


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
    print("任务解析完毕！")
    # 生成影片信息
    hls = open('hls.html', 'r')
    html = open('index.html', 'w')
    html.write(hls.read().replace('{name}', info[2]))
    hls.close()
    html.close()
    print("影片信息已生成！")


def add_tracker(url):
    r = requests.get(url)
    trackers = r.text.splitlines()
    tracker_list = []
    for i in trackers:
        if i:
            tracker_list.append(i)
    conf = open('aria2.conf', 'a+')
    conf.write(f"bt-tracker={tracker_list}")
    conf.close()
    with open('aria2.conf', 'r') as f:
        print(f.read())
    print("tracker添加完毕！")


if __name__ == '__main__':
    tracker_url = "https://ngosang.github.io/trackerslist/trackers_best.txt"
    setup()
    add_tracker(tracker_url)
