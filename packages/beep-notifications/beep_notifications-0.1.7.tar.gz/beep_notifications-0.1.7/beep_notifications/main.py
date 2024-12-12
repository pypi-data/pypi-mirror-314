from typing import Dict

import requests


class BeepNotify:
    def __init__(self, project):
        self.project = project
        self.api_root = 'https://beep.api.worldz.tech/api'

    def get_link_code(self):
        url = f"{self.api_root}/{self.project}/link/create/"
        resp = requests.post(url)

        res = resp.json()

        return res['code']

    def check_link_code(self, code):
        url = f"{self.api_root}/{self.project}/link/check/{code}/"
        resp = requests.get(url)
        res: Dict = resp.json()

        return res.get('accepted'), res.get('receiver'), res.get('username')

    def send_notification(self, title, body, username):
        url = f"{self.api_root}/notifications/{self.project}/{username}/"
        resp = requests.post(url, data={
            'title': title,
            'body': body,
        })

        return resp.status_code == 200

    def send_auth_code(self, username):
        url = f"{self.api_root}/auth/{self.project}/{username}/acode/"
        resp = requests.get(url)

        return resp.status_code == 200

    def get_token(self, username, code):
        url = f"{self.api_root}/auth/{self.project}/{username}/acode/"
        resp = requests.post(url, data={
            "code": code,
        })

        if resp.status_code == 200:
            return resp.json()['token']
        else:
            return None

    def validate_token(self, token, uac=False):
        url = f"{self.api_root}/auth/{self.project}/auth/"
        resp = requests.post(url, data={'token': token, 'uac': uac})

        res = resp.json()

        return resp.status_code == 200, res.get('beep'), res.get('error')
