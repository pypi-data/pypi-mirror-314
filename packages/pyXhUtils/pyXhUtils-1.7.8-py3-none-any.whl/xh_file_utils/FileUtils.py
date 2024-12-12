import os
from typing import Generator


class FileUtils:
    @staticmethod
    def read_file_lines(path) -> [Generator[str, None, None]]:
        FileUtils.check_file(path, check_is_file=True)
        with open(path) as f:
            for line in f:
                yield line

    @staticmethod
    def read_file(path) -> str:
        FileUtils.check_file(path, check_is_file=True)
        with open(path) as f:
            return f.read()

    @staticmethod
    def check_file(path, label="File", check_exists=False, check_is_file=False, check_is_directory=False, check_not_exists=False):
        if check_exists and not os.path.exists(path):
            raise Exception(f"File[{path}] not exists")
        if check_not_exists and os.path.exists(path):
            raise Exception(f"File[{path}] already exists")
        if check_is_file and not os.path.isfile(path):
            raise Exception(f"{label}[{path}] is not file")
        if check_is_directory and not os.path.isdir(path):
            raise Exception(f"{label}[{path}] is not directory")
        return True
