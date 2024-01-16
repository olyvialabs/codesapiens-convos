import os
from pathlib import Path
from parser.file.FileStructure import FileStructure
from config.exclude_file_by_extension import excluded_list_combined
from config.exclude_by_filename import exclude_file_list_by_filename


class FolderStructure:
    def __init__(self, folder_path, depth=0):
        self.absolute_path = folder_path
        current_folder = Path(self.absolute_path)
        self.path = str(folder_path)
        self.absolute_path = os.getcwd() + '/' + str(folder_path)
        self.name = current_folder.name
        self.files = self.get_files(folder_path, depth)
        self.folders = self.get_structure(folder_path, depth + 1)
        self.depth = depth + 1

    @staticmethod
    def get_files(dir, depth):
        dir_path = Path(dir)
        entries = [entry for entry in dir_path.iterdir()]
        files = []
        for entry in entries:
            if not entry.is_dir() and FolderStructure.should_document(entry, entry.is_dir()):
                files.append(FileStructure(dir, entry, depth))
        return files

    def get_files_instance(self, dir, depth):
        return FolderStructure.get_files(dir, depth)

    def get_structure(self, folder_path, depth):
        folders = []
        print(folder_path)
        print(folder_path)
        print(folder_path)
        dir_path = Path(folder_path)
        print(folder_path)
        entries = [entry for entry in dir_path.iterdir()]
        for entry in entries:
            if entry.is_dir() and FolderStructure.should_document(entry, entry.is_dir()):
                folders.append(FolderStructure(entry, depth))
        return folders

    @staticmethod
    def should_exclude(file_or_folder_path):
        path_object = Path(file_or_folder_path)
        file_size_in_bytes = path_object.stat().st_size
        doc_exceds_size = file_size_in_bytes > 0.5 * 1024 * 1024  # 1/2 MB

        if doc_exceds_size:
            return True

        filename = path_object.name
        filename_excluded = filename in exclude_file_list_by_filename
        if filename_excluded:
            return True

        extension = path_object.suffix[1:]  # remove the dot
        if extension:
            extension = extension.lower()
        return extension in excluded_list_combined

    @staticmethod
    def should_document(file_or_folder_path, is_directory):
        return is_directory or not FolderStructure.should_exclude(file_or_folder_path=file_or_folder_path)

    @staticmethod
    def get_folders_and_files(path):
        dir_path = Path(path)
        return [entry.name for entry in dir_path.iterdir()]
