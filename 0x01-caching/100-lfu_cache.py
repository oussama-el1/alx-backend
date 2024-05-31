#!/usr/bin/python3
"""
LFU caching
"""


BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):

    """
        class LFUCache
    """

    def __init__(self):
        """
        constractor
        """
        super().__init__()
        self.usage_history = {}  # {A: 0, B: 3, C: 4}

    def put(self, key, item):
        """ Put item in a cache storage with LFU caching algorithm """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.usage_history[key] += 1
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    min_usage = min(self.usage_history.values())
                    least_used_keys = [k for k, v in self.usage_history.items()
                                       if v == min_usage]

                    # Evict the first inserted least frequently used key
                    for k in self.cache_data.keys():
                        if k in least_used_keys:
                            least_used = k
                            break

                    del self.cache_data[least_used]
                    del self.usage_history[least_used]
                    print(f'DISCARD: {least_used}')

                # Add the new key with initial usage count of 1
                self.usage_history[key] = 1

            # Update cache data
            self.cache_data[key] = item

    def get(self, key):
        """ Retrieve item from cache storage """
        if key in self.cache_data:
            self.usage_history[key] += 1
            return self.cache_data[key]
        return None
