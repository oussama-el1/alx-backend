#!/usr/bin/env python3
"""
Basic dictionary
"""


BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """
        BasicCache class
    """
    def __init__(self):
        """
        constructor
        """
        super().__init__()

    def put(self, key, item):
        """
        put item in a cache
        """
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """
        get item from the cache by a key
        """
        if key is None:
            return None
        return self.cache_data.get(key, None)
