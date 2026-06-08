from collections import OrderedDict
import threading

class TranslationCache:

    def __init__(self, max_items=20000):
        self.max_items = max_items
        self.cache = OrderedDict()
        self.lock = threading.RLock()

    def get(self, key):

        with self.lock:

            value = self.cache.get(key)

            if value is not None:
                self.cache.move_to_end(key)

            return value

    def set(self, key, value):

        with self.lock:

            self.cache[key] = value
            self.cache.move_to_end(key)

            while len(self.cache) > self.max_items:
                self.cache.popitem(last=False)

    def clear(self):

        with self.lock:
            self.cache.clear()
