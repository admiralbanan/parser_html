import json

class Cache:
    def __init__(self, filename="cache.json"):
        self.filename = filename

    def save(self, key, data):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
        except FileNotFoundError:
            cache_data = {}

        cache_data[key] = data

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(cache_data, f)

    def load(self, key):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
                return cache_data.get(key)
        except FileNotFoundError:
            return None
