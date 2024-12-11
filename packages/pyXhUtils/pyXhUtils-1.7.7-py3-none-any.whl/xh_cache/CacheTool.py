import hashlib
import os
import sys
import typing


class DurableCache():
    def __init__(self, cache_name: str, with_log: bool = False):
        self.cache_name = f".cache_{cache_name}"
        self.with_log = with_log
        os.makedirs(self.cache_name, exist_ok=True)

    def get_cache(self, name: str, day_to_keep=14):
        return DurableCacheInDay(self.cache_name, name, day_to_keep, self.with_log)


class Logger():
    def __init__(self, output: typing.IO|None=None):
        self.output = output

    def write(self, text: str):
        if self.output is not None:
            self.output.write(text)
            self.output.write("\n")
            self.output.flush()

    @staticmethod
    def get_stderr_logger():
        return Logger(output=sys.stderr)

    @staticmethod
    def get_stdout_logger():
        return Logger(output=sys.stdout)

    def get_file_logger(self, name: str):
        return Logger(output=open(name, "w"))


class DurableCacheInDay():
    def get_path(self):
        return os.path.join(self.bash_path, self.cache_name)

    def __init__(self, bash_path, cache_name: str, day_to_key: int, with_log: bool = False):
        self.bash_path = bash_path
        self.cache_name = cache_name
        self.day_to_key = day_to_key
        self.with_log = with_log
        if self.with_log:
            self.logger = Logger.get_stderr_logger()
        os.makedirs(self.get_path(), exist_ok=True)


    def cache(self, key:str, get_data):
        key_gen=hashlib.sha256(key.encode("utf-8")).hexdigest()
        cached_file=os.path.join(self.get_path(),key_gen)
        import datetime as dt
        if os.path.exists(cached_file) and (dt.datetime.now() - dt.datetime.fromtimestamp(os.path.getctime(cached_file))).days < self.day_to_key:
            if self.with_log:
                self.logger.write(f"[{key}] already cached")
            return open(cached_file).read()
        else:
            self.logger.write(f"[{key}] not cached")
            data = get_data()
            open(cached_file, "w").write(data)
            return data

if __name__ == '__main__':
    logger=Logger.get_stderr_logger()
    logger.write("hihihi")