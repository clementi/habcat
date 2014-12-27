import requests
from models import Paginated


class HabstarClient(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def get_habstar(self, hip_num):
        response = requests.get(self.base_url + '/{}'.format(hip_num))
        if response.status_code == 404:
            return None
        return response.json()

    def get_habstars(self, page_num=1):
        response = requests.get(self.base_url + '/?p={}'.format(page_num))
        return Paginated(response.json())

    def get_habstars_by_distance(self, hip_num, dist=10, page_num=1):
        response = requests.get(self.base_url + '/?a=dist&p={}&r={}&d={}'.format(page_num, hip_num, dist))
        paginated = Paginated(response.json())
        paginated.items.sort(lambda x, y: cmp(float(x['ref_dist_pc']), float(y['ref_dist_pc'])))
        return paginated

    def get_habstars_with_similar_magnitude_to(self, magnitude, page_num=1):
        response = requests.get(self.base_url + '/?a=similar_mag&m={}&p={}'.format(magnitude, page_num))
        paginated = Paginated(response.json())
        paginated.items.sort(lambda x, y: cmp(float(x['mag']), float(y['mag'])))
        return paginated

    def get_habstars_with_similar_color_to(self, b_minus_v, page_num=1):
        response = requests.get(self.base_url + '/?a=similar_color&c={}&p={}'.format(b_minus_v, page_num))
        paginated = Paginated(response.json())
        paginated.items.sort(lambda x, y: cmp(float(x['bmv']['v']), float(y['bmv']['v'])))
        return paginated