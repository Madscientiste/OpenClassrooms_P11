import json
from pathlib import Path
from random import randint


DATA_FOLDER = Path(__file__).parent.parent / "data"


class JsonLoader:
    """Load a json from /data/, and handles basic operations"""

    def __init__(self, target, testing=False):
        self.target = target
        self.testing = testing
        self.values = self._load_json()

    def __iter__(self):
        return iter(self.values)

    def _load_json(self):
        with open(str(DATA_FOLDER / self.target) + ".json") as file:
            load_name = "test" if self.testing else self.target
            self.values = json.load(file)[load_name]
            return self.values

    def get_by(self, key, value, first=False):
        """Find an item by a key and value. Returns if nothing is found

        Arguments:
            key {str} -- The key to search by
            value {str} -- The value to search for, if a function is passed, it will be used to filter the values

        Keyword Arguments:
            first {bool} -- If True, return the first club found (default: {False})
        """

        if callable(value):
            found = iter([v for v in self.values if value(v[key])])
        else:
            found = filter(lambda x: x[key] == value, self.values)

        return next(found, None) if first else list(found)

    def get_random(self, key):
        """Get a random item by a key

        Arguments:
            key {str} -- The key to search by
        """
        return self.values[randint(0, len(self.values) - 1)][key]
