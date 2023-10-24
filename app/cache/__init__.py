import time


class Cache:
    def __init__(self, ttl="1d"):
        self.data = {}
        self.ttl = self.parse_ttl(ttl)

    def set(self, key, value, ttl=None):
        """Set a key-value pair in the cache with an optional custom TTL."""
        self.data[key] = {
            "value": value,
            "ttl": self.parse_ttl(ttl) if ttl is not None else self.ttl,
            "created_time": time.time(),
        }

    def get(self, key):
        """Get the value associated with a key from the cache."""
        if key in self.data:
            item = self.data[key]
            if self.is_valid(item):
                return item["value"]
            else:
                del self.data[key]
        return None

    def delete(self, key):
        """Delete a key from the cache."""
        if key in self.data:
            del self.data[key]

    def clear(self):
        """Clear all expired and non-expired data from the cache."""
        current_time = time.time()
        self.data = {
            key: item
            for key, item in self.data.items()
            if self.is_valid(item, current_time)
        }

    def is_valid(self, item, current_time=None):
        """Check if an item is still valid based on TTL."""
        if current_time is None:
            current_time = time.time()
        return item["created_time"] + item["ttl"] > current_time

    def parse_ttl(self, ttl):
        """Parse a TTL string to seconds (e.g., '1d' for 1 day)."""
        ttl_units = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 86400,
        }
        unit = ttl[-1]
        value = int(ttl[:-1])
        return value * ttl_units.get(unit, 1)
