#!/usr/bin/env python3
"""
LIFO caching
"""


BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache class for lifo cache algorithme
    """

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """
        put item in cash storage with a key
        """

        if key and item:
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                try:
                    beforelastkey = list(self.cache_data.keys())[-2]
                except IndexError:
                    beforelastkey = None
                if beforelastkey is not None:
                    del self.cache_data[beforelastkey]
                print(f'DISCARD: {beforelastkey}')

    def get(self, key):
        """
        get Item from cache by key
        """
        return self.cache_data.get(key, None)
