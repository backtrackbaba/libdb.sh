import json


class PackageParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        data = self._read_json()
        deps_dict = {}
        dev_deps = list(data.get("devDependencies", {}).keys())
        deps = list(data.get("dependencies", {}).keys())
        return set(deps + dev_deps)

    def _read_json(self):
        with open(self.file_path) as fp:
            data = json.load(fp)
        return data
