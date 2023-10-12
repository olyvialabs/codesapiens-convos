from llm.open_ai import get_gpt_response_from_template
from pathlib import Path
from parser.file.ProjectStructure import ProjectStructure
from parser.file.FolderStructure import FolderStructure
from config.documents_by_extension import list_of_accepted_docs_file_extensions
import json
from config.settings import settings
import re
import os


def get_package_json_data_for_dependencies(filename: str = 'package.json'):
    with open(filename, 'r') as file:
        data = json.load(file)

        dependencies = data.get('dependencies', {})
        dev_dependencies = data.get('devDependencies', {})

        dependencies_mixed = 'Dependencies:\n'
        for name, version in dependencies.items():
            dependencies_mixed = dependencies_mixed + \
                f"{name}: {version}\n"
        dependencies_mixed = '\ndevDependencies:\n'
        for name, version in dev_dependencies.items():
            dependencies_mixed = dependencies_mixed + \
                f"{name}: {version}\n"
        return_data = {
            'name': data.get('name', ''),
            'trimmable_content': dependencies_mixed
        }
        return return_data


def get_package_json_data(filename: str = 'package.json'):
    with open(filename, 'r') as file:
        data = json.load(file)

        scripts = data.get('scripts', {})

        scripts_mixed = ''
        for name, script in scripts.items():
            scripts_mixed = scripts_mixed + \
                f"{name}: {script}\n"
        return_data = {
            'trimmable_content': scripts_mixed,
            'name': data.get('name', ''),
            'version': data.get('version', ''),
            'description': data.get('description', ''),
            'author': data.get('author', ''),
            'license': data.get('license', ''),
            'homepage': data.get('homepage', ''),
        }
        return return_data


def generate_root_config_files(config_list=[], project_name=''):
    for config in config_list:
        # this path comes from "what_are_these_config_files" JSON
        file_name = config['path']
        file_name_path = Path(file_name)
        print(f'Now processing: ${file_name} {file_name_path.as_uri()}')
        configuration_folder_path = project_name+'/Configuration'
        if config['isConfig']:
            config_list = get_gpt_response_from_template(
                data={'project_name': project_name, 'file_name': file_name}, template='general_config', trim_content=True, trim_path=file_name, save_to_subfolder=configuration_folder_path, save_to_name=file_name_path.stem + '.md')
        elif config['isAppSpecific']:
            config_list = get_gpt_response_from_template(
                data={'project_name': project_name, 'file_name': file_name}, template='app_config', trim_content=True, trim_path=file_name, save_to_subfolder=configuration_folder_path, save_to_name=file_name_path.stem + '.md')
        elif config['isCodeRelated']:
            config_list = get_gpt_response_from_template(
                data={'file_name': file_name}, template='parse_root_code_document', trim_content=True, trim_path=file_name, save_to_subfolder=configuration_folder_path, save_to_name=file_name_path.stem + '.md')


def _read_content_from_path(absolute_path):
    with open(absolute_path, 'r') as file:
        return file.read()


def generate_documentation_for_project_per_file(project: ProjectStructure, project_name=''):
    all_files = project.get_all_files(keep_root_files=False)
    current_dir = Path(os.getcwd())
    for file in all_files:
        print(f'Now processing file: ${file.entry}')
        temp_file_path = Path(file.absolute_path)
        file_extension = temp_file_path.suffix[1:]  # remove the dot

        result_path = current_dir.joinpath(temp_file_path.parent)
        result_path_str = str(result_path)

        result_path_str = result_path_str.replace(
            settings.temp_folder+'/'+project_name, settings.output_folder+'/'+project_name)
        # if file_extension in temp_file_path.name.endswith('package.json'):
        error = None
        if temp_file_path.name.endswith('package.json'):
            _, error = get_gpt_response_from_template(
                data=get_package_json_data(file.absolute_path), template='parse_package_json', trim_content=True, save_to_subfolder=result_path_str, save_to_name=temp_file_path.stem + '.md', ignore_output_folder_on_save=True)
            if not error:
                _, error = get_gpt_response_from_template(
                    data=get_package_json_data_for_dependencies(file.absolute_path), template='parse_package_json_dependencies', trim_content=True, save_to_subfolder=result_path_str, save_to_name=temp_file_path.stem + '_dependencies' + '.md', ignore_output_folder_on_save=True)
        elif file_extension in list_of_accepted_docs_file_extensions:
            _, error = get_gpt_response_from_template(
                data={'file_name': file.name}, template='parse_document_file', trim_content=True, trim_path=file.absolute_path, save_to_subfolder=result_path_str, save_to_name=temp_file_path.stem + '.md', ignore_output_folder_on_save=True)
        else:
            _, error = get_gpt_response_from_template(
                data={'file_name': file.name}, template='document_file_prompt', trim_content=True, trim_path=file.absolute_path, save_to_subfolder=result_path_str, save_to_name=temp_file_path.stem + '.md', ignore_output_folder_on_save=True)
        if error:
            print(f'Error: {error}')


def get_file_summary(file_absolute_path):
    file_content = _read_content_from_path(file_absolute_path)
    regex = re.compile(r'^# .+[\s\S]*?^## .+', re.MULTILINE)
    match = regex.search(file_content)

    if match:
        return match.group(0).strip()

    if len(file_content) > 350:
        return file_content[:350] + '...'

    return file_content


def get_folder_summary(folder_absolute_path):
    # TODO: this is currently always empty as we are not having
    # the folders correctly in order, so when we arrive to the folder we don't have the files
    # it should be fixed in the future
    # solution: folder retrieval should be back-to-front instead of right now front-to-back

    return ''


def generate_documentation_for_project_per_folder(project: ProjectStructure, project_name=''):
    all_folders = project.get_all_folders().reverse()
    print(all_folders)
    root_path = Path(f"{settings.output_folder}/{project_name}")
    for folder in all_folders:
        print(f'Now processing folder: ${folder.path}')
        temp_project_struct = FolderStructure(folder_path=folder.path)
        list_of_files_listed_in_folder = []
        for file in temp_project_struct.files:
            file_path_obj = Path(file.path)

            # Get the relative path from the root
            relative_path = file_path_obj.relative_to(root_path)
            list_of_files_listed_in_folder.append(
                {'name': file.name, 'path': str(relative_path), 'fileOrFolder': 'file', 'summary': get_file_summary(file.absolute_path)})
        for inner_folder in temp_project_struct.folders:
            folder_path_obj = Path(inner_folder.path)

            # Get the relative path from the root
            relative_path = folder_path_obj.relative_to(root_path)
            list_of_files_listed_in_folder.append(
                {'name': inner_folder.name, 'path': str(relative_path), 'fileOrFolder': 'folder', 'summary': get_folder_summary(inner_folder.absolute_path)})
        query_content = json.dumps(list_of_files_listed_in_folder)
        get_gpt_response_from_template(
            data={'mdFileName': folder.name, 'trimmable_content': query_content}, template='parse_folder_document', trim_content=True, save_to_subfolder=folder.path, save_to_name=folder.name + '.md', ignore_output_folder_on_save=True)
