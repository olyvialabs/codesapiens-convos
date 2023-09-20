import os
from pathlib import Path


class FileStructure:

    def __init__(self, dir, entry, depth):
        self.name = entry.name
        project_path = Path.cwd()
        self.path = os.path.relpath(
            os.path.join(dir, entry.name), project_path)
        self.entry = entry
        self.depth = depth
        self.directory = dir

    @staticmethod
    def get_content(path_str):
        if not os.path.exists(path_str):
            print(f"path:{path_str} not found, returning empty string")
            return ''

        if os.path.isdir(path_str):
            return ''

        with open(path_str, 'r') as file:
            return file.read()
