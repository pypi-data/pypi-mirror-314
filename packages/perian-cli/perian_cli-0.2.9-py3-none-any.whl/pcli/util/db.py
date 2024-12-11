import json
import os

from pcli.util import get_perian_config_directory


class DB:
    db_file: str = "db.json"
    db_file_path: str

    def __init__(self):
        self.db_file_path = os.path.join(get_perian_config_directory(), self.db_file)

    def _exists(self):
        return os.path.exists(self.db_file_path)

    def _store(self, data):
        with open(self.db_file_path, "w") as outfile:
            json.dump(data, outfile)

    def get(self, key):
        if self._exists():
            f = open(self.db_file_path)
            data = json.load(f)
            if key in data:
                return data[key]
            else:
                return None
        else:
            return None

    def set(self, key, value):
        if self._exists():
            f = open(self.db_file_path)
            data = json.load(f)
            data[key] = value
            self._store(data)
        else:
            data = {}
            data[key] = value
            self._store(data)

    def clear(self):
        if self._exists():
            os.remove(self.db_file_path)
