#!/usr/bin/env python3
"""
MRU Caching
"""


BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache class implements an MRU caching mechanism.
    """
    def __init__(self):
        super().__init__()
        self.history = []

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key and item:
            if key in self.history:
                self.history.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lru_key = self.history.pop(-1)
                del self.cache_data[lru_key]
                print(f'DISCARD: {lru_key}')
            self.cache_data[key] = item
            self.history.append(key)

    def get(self, key):
        """
        Get an item by key
        """
        if key in self.cache_data:
            self.history.remove(key)
            self.history.append(key)
        return self.cache_data.get(key, None)
