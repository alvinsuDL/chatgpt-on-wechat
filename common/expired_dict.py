import time


class ExpiredDict(dict):
    def __init__(self, expires_in_seconds):
        super().__init__()
        self.expires_in_seconds = expires_in_seconds

    def __getitem__(self, key):
        value, expiry_time = super().__getitem__(key)
        # 如果元素已过期，则从字典中删除该元素并抛出 KeyError 异常
        if time.monotonic() > expiry_time:
            del self[key]
            raise KeyError("expired {}".format(key))
        self.__setitem__(key, value)
        return value

    def __setitem__(self, key, value):
        # 刷新元素缓存时间
        super().__setitem__(key, (value, time.monotonic() + self.expires_in_seconds))

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
