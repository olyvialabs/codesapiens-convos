from llm.open_ai import get_gpt_response_from_template
from pathlib import Path
from parser.file.ProjectStructure import ProjectStructure
from config.documents_by_extension import list_of_accepted_docs_file_extensions


def generate_root_config_files(config_list=[], project_name=''):
    for config in config_list:
        file_name = config['path']
        file_name_path = Path(file_name)
        if config['isConfig']:
            config_list = get_gpt_response_from_template(
                data={'project_name': project_name, 'file_name': file_name}, template='general_config', trim_content=True, trim_path=file_name, save_to_subfolder='/Configuration', save_to_name=file_name_path.stem + '.md')
        elif config['isAppSpecific']:
            config_list = get_gpt_response_from_template(
                data={'project_name': project_name, 'file_name': file_name}, template='app_config', trim_content=True, trim_path=file_name, save_to_subfolder='/Configuration', save_to_name=file_name_path.stem + '.md')
        elif config['isCodeRelated']:
            config_list = get_gpt_response_from_template(
                data={'file_name': file_name}, template='document_file_prompt', trim_content=True, trim_path=file_name, save_to_subfolder='/Configuration', save_to_name=file_name_path.stem + '.md')


def generate_documentation_to_all_inner_folders(project: ProjectStructure):
    all_files = project.get_all_files(keep_root_files=False)
    for file in all_files:
        print(f'Now processing: ${file.entry}')
        if file.get_content(file.path):
            temp_file_path = Path(file.path)
            file_extension = temp_file_path.suffix[1:]  # remove the dot
            if file_extension in list_of_accepted_docs_file_extensions:
                get_gpt_response_from_template(
                    data={'file_name': file.name}, template='parse_document_prompt', trim_content=True, trim_path=file.path, save_to_subfolder=temp_file_path.parent, save_to_name=temp_file_path.stem + '.md')
            else:
                get_gpt_response_from_template(
                    data={'file_name': file.name}, template='document_file_prompt', trim_content=True, trim_path=file.path, save_to_subfolder=temp_file_path.parent, save_to_name=temp_file_path.stem + '.md')
    return
