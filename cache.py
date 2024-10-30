import json

class Cache:
    def __init__(self, filename="cache.json"):
        self.filename = filename

    def save(self, key, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump({key: data}, f)

    def load(self, key):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(key, None)
        except FileNotFoundError:
            return None

    def clear(self, key):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump({}, f)
