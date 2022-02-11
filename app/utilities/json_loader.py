import json
from pathlib import Path
from random import randint


DATA_FOLDER = Path(__file__).parent.parent / "data"


class JsonLoader:
    """Load a json from /data/, and handles basic operations"""

    def __init__(self, target):
        self.target = target
        self.values = self._load_json()

    def __iter__(self):
        return iter(self.values)

    def _load_json(self):
        with open(str(DATA_FOLDER / self.target) + ".json") as file:
            self.values = json.load(file)[self.target]
            return self.values

    def _update_json(self):
        with open(str(DATA_FOLDER / self.target) + ".json", "w") as file:
            json.dump(self.values, file)

    def get_by(self, key, value, first=False):
        """Find an item by a key and value. Returns if nothing is found

        Arguments:
            key {str} -- The key to search by
            value {str} -- The value to search for

        Keyword Arguments:
            first {bool} -- If True, return the first club found (default: {False})
        """
        found = filter(lambda x: x[key] == value, self.values)
        return next(found, None) if first else list(found)

    def get_random(self, key):
        """Get a random item by a key

        Arguments:
            key {str} -- The key to search by
        """
        return self.values[randint(0, len(self.values) - 1)][key]
