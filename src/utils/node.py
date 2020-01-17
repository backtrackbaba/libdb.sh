import os

import requests
from walrus import Database

from utils.parsers.package_parser import PackageParser

base_url = "https://replicate.npmjs.com"

db = Database(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'), db=os.environ.get('REDIS_DB'),
              password=os.environ.get('REDIS_PASSWORD'))

cache = db.cache()

WEEKS_IN_SECONDS = 60 * 60 * 24 * 7


class NodeUtil:

    def parse_package(self, package_path):
        package_parser = PackageParser(package_path)
        package_data = package_parser.parse()
        return package_data

    def fetch_info(self, package_list: list) -> dict:
        info_dict = {}
        for req in package_list:
            info = self.fetch_npm(req)
            info_dict[req] = info
        return info_dict

    @cache.cached(timeout=WEEKS_IN_SECONDS)
    def fetch_npm(self, name: str):
        url = f"{base_url}/{name}"
        r = requests.get(url)
        lib_data = r.json()
        required_data = self._prepare_lib_data(lib_data)
        return required_data

    def _prepare_lib_data(self, lib: dict):
        required_data = {}
        required_data.update({
            'url': lib['homepage'],
            'name': lib['name'],
            'summary': lib['description'],
            'version': lib['dist-tags']['latest'],
            'license': lib['license'],
        })
        return required_data
