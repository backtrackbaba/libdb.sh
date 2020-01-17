import os

import requests
import requirements
from walrus import *

base_url = "https://pypi.org/pypi"

db = Database(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'), db=os.environ.get('REDIS_DB'),
              password=os.environ.get('REDIS_PASSWORD'))
cache = db.cache()

WEEKS_IN_SECONDS = 60 * 60 * 24 * 7


class PypiUtil:

    def parse_requrements(self, requirement_path) -> list:
        request_names = []
        with open(requirement_path, 'r') as fd:
            for req in requirements.parse(fd):
                request_names.append(req.name)
        return request_names

    def fetch_info(self, requirements_list: list) -> dict:
        info_dict = {}
        for req in requirements_list:
            info = self.fetch_lib(req)
            info_dict[req] = info
        return info_dict

    @cache.cached(timeout=WEEKS_IN_SECONDS)
    def fetch_lib(self, name: str):
        url = f"{base_url}/{name}/json"
        r = requests.get(url)
        lib_data = r.json()
        required_data = self._prepare_lib_data(lib_data)
        return required_data

    def _prepare_lib_data(self, lib: dict):
        required_data = {}
        required_data.update({
            'url': lib['info']['home_page'],
            'name': lib['info']['name'],
            'summary': lib['info']['summary'],
            'version': lib['info']['version'],
            'license': lib['info']['license'],
        })
        return required_data
