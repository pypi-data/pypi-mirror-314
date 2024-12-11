import hashlib
import json
import os


class DurableCache():
    def __init__(self, cache_name: str):
        self.cache_name = f".cache_{cache_name}"
        os.makedirs(self.cache_name, exist_ok=True)

    def get_cache(self, name: str, day_to_keep):
        return DurableCacheInDay(self.cache_name, name, day_to_keep)



class DurableCacheInDay():
    def get_path(self):
        return os.path.join(self.bash_path, self.cache_name)

    def __init__(self, bash_path, cache_name: str, day_to_key: int):
        self.bash_path = bash_path
        self.cache_name = cache_name
        self.day_to_key = day_to_key
        os.makedirs(self.get_path(), exist_ok=True)


    def cache(self, key:str, get_data):
        key_gen=hashlib.sha256(key.encode("utf-8")).hexdigest()
        cached_file=os.path.join(self.get_path(),key_gen)
        import datetime as dt
        if os.path.exists(cached_file) and (dt.datetime.now() - dt.datetime.fromtimestamp(os.path.getctime(cached_file))).days < self.day_to_key:
            return json.loads(open(cached_file).read())["results"]
        else:
            data = get_data()
            open(cached_file, "w").write(data)
            return data
