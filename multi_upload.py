import os
import requests
import base64
from threading import Thread

def create_repo(name, token):
    url = 'https://api.github.com/user/repos'
    data = {"name": name, "private": False}
    header = {'Authorization': f'token {token}'}
    r = requests.post(url, headers = header, json = data)
    print(r.status_code, r.json()["ssh_url"])
    return r.json()["ssh_url"]


def upload(owner, token, repo, local_path, remote_path):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{remote_path}'
    header = {'Authorization': f'token {token}'}
    f = open(local_path, 'rb')
    data_b64 = base64.b64encode(f.read())
    f.close()
    data = {'message':'upload by ghcdn', 'content': data_b64}
    r = requests.put(url, json = data, headers= header)
    print(r.status_code, r.json()['content']['download_url'])
    return r.json()['content']['download_url']

def multi_upload(owner, token, repo,file_list):
    for file in file_list:
        upload(owner, token, repo, file, file)


def get_filelist(dir_path):
    file_list = []
    for home, dirs, files in os.walk(dir_path):
        for filename in files:
            fullname = os.path.join(home, filename)
            file_list.append(fullname)
    return file_list


if __name__ == '__main__':
    owner = 'ghcdn'
    repo = 'repo name'
    token = 'your github token'
    threads = 16
    filepath = 'some'
    file_list = get_filelist(filepath)
    thread_pool = []
    thread_num = len(file_list)//threads

    for i in range(threads-1):
        start = i*thread_num
        end = (i+1)*thread_num
        t = Thread(target=multi_upload, args=(owner, token,repo, file_list[start:end]))
        thread_pool.append(t)
    # 最后一部分
    start = (threads - 1)*thread_num
    end = len(file_list)
    t = Thread(target=multi_upload, args=(owner, token, repo, file_list[start:end]))
    thread_pool.append(t)
    # 启动所有子线程
    for t in thread_pool:
        t.start()
    # 子线程合并到主线程
    for t in thread_pool:
        t.join()
    print(f'All work done! view in \
          https://cdn.jsdelivr.net/gh/{owner}/{repo}/{filepath}/index.m3u8')
