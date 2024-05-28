#!/usr/bin/env python3
"""
LRU Caching
"""


BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """
    class LRUCache
    """

    def __init__(self):
        """
        constractor
        """
        super().__init__()
        self.history = []

    def put(self, key, item):
        """
        Put to a cache data a item
        """
        if key and item:
            self.cache_data[key] = item
            self.history.append(key)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                lru_key = self.history[0]
                del self.cache_data[lru_key]
                print(f'DISCARD: {lru_key}')
                self.history.remove(lru_key)

    def get(self, key):
        """
        get item from cache Storage
        """
        if key in self.history:
            self.history.remove(key)
        if len(self.history) >= 4:
            self.history[-1] = key
        else:
            self.history.append(key)
        return self.cache_data.get(key, None)
