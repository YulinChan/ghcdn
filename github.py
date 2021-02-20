import requests
import base64


class Github:
    def __init__(self, name, token):
        self.owner = name
        self.token = token
        self.header = {'Authorization': f'token {self.token}'}

    def create_repo(self, name):
        url = 'https://api.github.com/user/repos'
        data = {"name": name, "private": False}
        r = requests.post(url, headers = self.header, json = data)
        print(r.status_code, r.json()["ssh_url"])
        return r.json()["ssh_url"]

    def delete_repo(self, name):
        url = f'https://api.github.com/repos/{self.owner}/{name}'
        r = requests.delete(url, headers=self.header)
        print(r.status_code)
        return r.status_code

    def upload(self, repo_name, local_path, remote_path, commit_msg):
        url = f'https://api.github.com/repos/{self.owner}/{repo_name}/contents/{remote_path}'
        f = open(local_path, 'rb')
        data_b64 = base64.b64encode(f.read())
        f.close()
        data = {'message':commit_msg, 'content': data_b64}
        r = requests.put(url, json = data, headers=self.header)
        print(r.status_code, r.json()['content']['download_url'])
        return r.json()['content']['download_url']

if __name__ == '__main__':
    me = Github('your github name', "your github token")
