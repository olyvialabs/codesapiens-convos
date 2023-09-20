from pathlib import Path
from parser.file.FolderStructure import FolderStructure


class ProjectStructure:
    def __init__(self, target_path=None):
        # Using os module for getting the current working directory
        self.project_path = target_path
        self.folder_structure = FolderStructure(self.project_path)

    def get_structure(self):
        return self.folder_structure

    def get_all_files(self):
        files = self.folder_structure.files
        for folder in self.folder_structure.folders:
            files.extend(self._get_subfiles(folder))
        return files

    def _get_subfiles(self, folder: FolderStructure):
        files = folder.files
        for subfolder in folder.folders:
            files.extend(self._get_subfiles(subfolder))
        return files
