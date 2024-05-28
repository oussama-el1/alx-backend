#!/usr/bin/env python3
"""
FIFO caching
"""


BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFO Cache Algorithme
    """

    def __init__(self):
        """
        constructor
        """
        super().__init__()

    def put(self, key, item):
        """
        Put in the cache
        """

        if key and item:
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                firstkey = next(iter(self.cache_data), None)
                del self.cache_data[firstkey]
                print(f'DISCARD: {firstkey}')

    def get(self, key):
        """
        get Item from cache by key
        """
        return self.cache_data.get(key, None)
