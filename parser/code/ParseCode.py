from llm.open_ai import get_gpt_response_from_template
from pathlib import Path
from parser.file.ProjectStructure import ProjectStructure


def generate_root_config_files(config_list=[], project_name=''):
    for config in config_list:
        file_name = config['path']
        file_name_path = Path(file_name)
        if config['isConfig']:
            config_list = get_gpt_response_from_template(
                data={'project_name': project_name, 'file_name': file_name}, template='general_config', trim_content=True, trim_path=file_name, save_to_subfolder='/Configuration', save_to_name=file_name_path.name)
        if config['isAppSpecific']:
            config_list = get_gpt_response_from_template(
                data={'project_name': project_name, 'file_name': file_name}, template='app_config', trim_content=True, trim_path=file_name, save_to_subfolder='/Configuration', save_to_name=file_name_path.name)


def generate_documentation_to_all_inner_folders(project: ProjectStructure):
    all_files = project.get_all_files()
    for file in all_files:
        print(f'${file.depth}:${file.entry}')
        if file.get_content(file.path):
            temp_file_path = Path(file.path)
            get_gpt_response_from_template(
                data={'file_name': file.name}, template='document_file_prompt', trim_content=True, trim_path=file.path, save_to_subfolder=temp_file_path.parent, save_to_name=temp_file_path.stem + '.md')
    # for file_structure in all_fil es:
    #   print(file_structure)
    # for folder in project.get_structure().folders:
    #     print(folder.get)
    # for file in project.get_structure().files:
    #     print(file)
    return
