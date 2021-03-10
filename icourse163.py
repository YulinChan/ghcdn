import sys
import time
import uuid
import random
import requests
from faker import Faker
from requests_toolbelt import MultipartEncoder


def get_token(csrfKey, fileName):
    ua = {"User-Agent": Faker().user_agent(),
          'X-Forwarded-For': Faker().ipv4()}
    url = 'https://www.icourse163.org/uploaderAccess/getUploaderVideoToken'
    params = {"csrfKey": csrfKey,
              "fileName": fileName, "type": "5",
              "fileSize": random.randrange(1000, 9999),
              "fileGmtModifiedTime": int(time.time() * 1000)}
    r = requests.get(url, params=params, headers=ua)
    return r.json()["result"]


def get_xnostoken(token, fileName):
    ua = {"User-Agent": Faker().user_agent(),
          'X-Forwarded-For': Faker().ipv4()}
    url = "https://up.study.163.com/j/uploader-server/UploaderCenterManager/exchangeNosTokenByEduToken.do"
    params = {"eduUploaderToken": token, "fileName": fileName,
              "fileSize": random.randrange(1000, 9999),
              "fileGmtModifiedTime": int(time.time() * 1000),
              '_t': int(time.time() * 1000)}
    r = requests.get(url, headers=ua, params=params)
    res = r.json()["result"]
    return res["nosKey"], res["xnosToken"]


def upload(nosKey, xnostoken, name, filePath):
    ua = {'User-Agent': Faker().user_agent(),
          'X-Forwarded-For': Faker().ipv4()}
    url = "https://nos.netease.com/edu-image"
    payload = {"Object": nosKey, "x-nos-token": xnostoken,
               "file": (name, open(filePath, 'rb'), 'image/png')}
    m = MultipartEncoder(payload)
    ua.update({'Content-Type': m.content_type})
    r = requests.post(url, data=m, headers=ua)
    res = r.json()
    return res["Bucket"] + '/' + res["NosKey"]


def main(csrfKey, filePath):
    name = f'{uuid.uuid4()}.png'
    token = get_token(csrfKey, name)
    nosKey, xnosToken = get_xnostoken(token, name)
    pic = upload(nosKey, xnosToken, name, filePath)
    url = "https://nos.netease.com/" + pic
    print(url)
    return url


if __name__ == '__main__':
    csrfKey = sys.argv[1]
    index = open('index.m3u8', 'r')
    res = open('playlist.m3u8', 'a')
    for line in index.readlines():
        if '#EXT' in line:
            res.write(line)
        else:
            file = line.strip()
            url = main(csrfKey, file)
            res.write(url + '\n')
            time.sleep(random.randrange(1, 3))
    index.closed()
    res.closed()
    print("video upload done!")
    print("video playlist:")
    playlist = main(csrfKey, 'playlist.m3u8')
    with open('online.txt', 'w') as f:
        f.write(playlist)
    print("All done!")
