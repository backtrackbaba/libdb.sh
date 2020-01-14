import requests
from walrus import Database

from src.utils.parsers.package_parser import PackageParser

base_url = "https://replicate.npmjs.com"

db = Database(host="localhost", port=6379, db=50,
              password="greyatom")
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
        return r.json()
