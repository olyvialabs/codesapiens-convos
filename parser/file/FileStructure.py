import os
from pathlib import Path


class FileStructure:

    def __init__(self, dir, entry, depth):
        self.name = entry.name
        self.path = os.path.join(dir, entry.name)
        self.absolute_path = os.getcwd() + '/' + os.path.join(dir, entry.name)

        self.entry = entry
        self.depth = depth
        self.directory = dir

    @staticmethod
    def get_content(path_str: str):
        if not os.path.exists(path_str):
            print(f"path:{path_str} not found, returning empty string")
            return ''

        if os.path.isdir(path_str):
            return ''

        with open(path_str, 'r') as file:
            return file.read()
