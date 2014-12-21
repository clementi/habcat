import requests


class HabstarClient(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def get_habstar(self, hip_num):
        response = requests.get(self.base_url + '/{}'.format(hip_num))
        if response.status_code == 404:
            return None
        return response.json()