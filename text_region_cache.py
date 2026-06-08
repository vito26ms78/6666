import time

class TextRegionCache:

    def __init__(self, ttl=5.0):

        self.ttl = ttl
        self.cache = {}

    def get(self, key):

        item = self.cache.get(key)

        if item is None:
            return None

        value, ts = item

        if time.time() - ts > self.ttl:
            self.cache.pop(key, None)
            return None

        return value

    def set(self, key, value):

        self.cache[key] = (
            value,
            time.time()
        )

    def cleanup(self):

        now = time.time()

        expired = [
            k
            for k, (_, ts)
            in self.cache.items()
            if now - ts > self.ttl
        ]

        for k in expired:
            self.cache.pop(k, None)
