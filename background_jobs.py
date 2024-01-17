from parser.file.ProjectStructure import ProjectStructure
from parser.file.FolderStructure import FolderStructure
from parser.code.RepoHandling import clone_repo_to_folder
from llm.open_ai import get_gpt_response_from_template
from config.settings import settings
import json
from llm.embeeding import embeed_md_files_to_store, embeed_github_files_to_store
from persister.supabase import update_process_end_date_and_logs, insert_process, get_user, get_unsynced_repository_docs, get_project_by_id
from logger.Logger import Logger
import logging
import os
import shutil
from celery import Celery
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from parser.file.ProjectStructure import ProjectStructure
from config.settings import settings
from datetime import datetime
from pathlib import Path
from config.documents_by_extension import list_of_accepted_docs_file_extensions
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback


celery = Celery()
celery.config_from_object("config.celery_config")
temp_absolute_dir = os.path.join(os.getcwd(), settings.temp_folder)
outputs_absolute_dir = os.path.join(os.getcwd(), settings.output_folder)


def process_files_in_batches(all_files, project_name, output_logger, batch_size=12):
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        # Start the first batch of tasks
        futures = [executor.submit(
            process_file, file, project_name, output_logger) for file in all_files[:batch_size]]

        # Process the rest of the files
        for i in range(batch_size, len(all_files)):
            # Wait for any future to complete before submitting the next one
            done = next(as_completed(futures))
            futures.remove(done)

            # Submit the next task
            next_file = all_files[i]
            future = executor.submit(
                process_file, next_file, project_name, output_logger)
            futures.append(future)

        # Wait for all remaining tasks to complete
        for future in as_completed(futures):
            pass  # Optionally handle results or exceptions here


def get_process_status(process_id):
    return {"status": "FINISHED", "details": "FINISHED"}
    # process = AsyncResult(process_id)

    # return {"status": process.status, "details": process.info}


def save_db_docs_to_temp_folder(logger, file_list, project_name):
    files = {}

    for file in file_list:
        full_path = temp_absolute_dir + '/' + project_name + '/' + \
            file['path'] + file['id']
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Write the file's content
        with open(full_path, 'w') as f:
            f.write(file['content'])
            file_id = file['id']
            file_path = file['path']
            files[f'{file_path}{file_id}.md'] = file_id
    return files


def process_github_repository(process_id, logger, project_name, repository, user, repoOrgName, repoName, id_project):
    clone_repo_to_folder(user['githubInstallationId'],
                         project_name, repoOrgName, repoName)

    output_logger = logging.getLogger(project_name)
    output_logger.addHandler(logger)
    output_logger.info("Starting analysis of " +
                       project_name.replace('|', '/')+"...")

    project = ProjectStructure(
        target_path=settings.temp_folder+'/'+project_name)
    project_main_folder = FolderStructure(
        settings.temp_folder+'/'+project_name)

    # Generates a JSON with all config files classified
    list_of_files_concatenated = ''
    for file_structure in project_main_folder.files:
        list_of_files_concatenated += file_structure.absolute_path + '\n'

    output_logger.info("Getting root configuration metadata...")
    # config_list = get_gpt_response_from_template(
    #     data={'app_name': project_name, 'trimmable_content': list_of_files_concatenated}, template='what_are_these_config_files', trim_content=True)
    # try:
    #     print('**********')
    #     print('THIS IS THE CONFIG', config_list)
    #     print('**********')
    #     config_list = json.loads(config_list[0])
    #     output_logger.info(
    #         "Root configuration metadata retrieved successfully.")

    #     output_logger.info("Generating root configuration...")
    #     # Based on the JSON, generate the documentation for each config file
    #     generate_root_config_files(
    #         config_list=config_list, project_name=project_name)
    #     output_logger.info("Root configuration generated successfully.")
    # except Exception as e:
    #     print(e)
    #     print(e)
    #     output_logger.info("Root configuration metadata skipped.")
    #     config_list = []

    output_logger.info(
        "Processing and generating documentation from repository...")
    # Generate all documentation per file
    processing_files = project.get_all_files(keep_root_files=False)
    process_files_in_batches(processing_files, project_name, output_logger)
    # generate_documentation_for_project_per_file(
    #     project=project, project_name=project_name, output_logger=output_logger)
    output_logger.info(
        "Documentation from repository processed and generated successfully.")

    if False:
        output_logger.info("Indexing each folder...")
        # Generate documentation for all folders
        output_project = ProjectStructure(
            target_path=settings.output_folder+'/'+project_name)
        generate_documentation_for_project_per_folder(
            project=output_project, project_name=project_name, output_logger=output_logger)
        output_logger.info("Folders indexed successfully.")

    # Generate indexes
    output_logger.info("Updating indexed data...")
    output_project_for_indexing = ProjectStructure(
        target_path=outputs_absolute_dir+'/'+project_name)
    raw_docs = []
    all_files = output_project_for_indexing.get_all_files(False)
    length_of_all_files = len(all_files)

    for file in all_files:
        print('File outputs processing path', file.path)
        abs_folder_path = os.path.join(os.getcwd(), file.path)
        parts = file.path.split("/")

        # Find the index of the first occurrence of "convos"
        try:
            outputs_index = parts.index(settings.output_folder)
        except ValueError:
            output_logger.error(f"'outputs' not found in path: {file.path}")
            continue  # Skip this file if 'outputs' is not in the path

        # Extract the path from "outputs" and forward
        # 1 because:
        # 0 would be outputs
        # 1 would be outputs/project_name
        # Extract the path from "outputs" and forward
        rel_path = "/".join(parts[outputs_index+1:])
        raw_docs.append(
            {"abs_path": settings.output_folder+'/'+project_name+'/'+file.path, "path": rel_path, "content": file.get_content(abs_folder_path)})
    embeed_github_files_to_store(
        repository, project_name, user['id'], process_id, id_project)

    output_logger.info("Indexed data successfully updated.")
    output_logger.info("Process finished.")

    # Delete created temp & output folder
    # if os.path.exists(temp_absolute_dir + '/' + project_name):
    #     shutil.rmtree(temp_absolute_dir + '/' + project_name)
    # if os.path.exists(outputs_absolute_dir + '/' + project_name):
    #     shutil.rmtree(outputs_absolute_dir + '/' + project_name)
    # self.update_state(state='FINISHED')
    output_logger.removeHandler(logger)
    return length_of_all_files


def process_normal_repository(process_id, user, repository_id, logger, project_name, files_map, project_id):
    output_logger = logging.getLogger(project_name)
    output_logger.addHandler(logger)
    output_logger.info("Starting analysis of " + project_name+"...")

    project = ProjectStructure(
        target_path=settings.temp_folder+'/'+project_name)
    project_main_folder = FolderStructure(
        settings.temp_folder+'/'+project_name)

    # Generates a JSON with all config files classified
    list_of_files_concatenated = ''
    for file_structure in project_main_folder.files:
        list_of_files_concatenated += file_structure.absolute_path + '\n'

    output_logger.info(
        "Processing and generating documentation from repository...")
    # Generate all documentation per file
    all_files = project.get_all_files(keep_root_files=False)
    process_files_in_batches(all_files, project_name, output_logger)
    # generate_documentation_for_project_per_file(
    #     project=project, project_name=project_name, output_logger=output_logger)
    output_logger.info(
        "Documentation from repository processed and generated successfully.")

    output_logger.info("Indexing each folder...")
    # Generate documentation for all folders
    output_project = ProjectStructure(
        target_path=settings.output_folder+'/'+project_name)
    generate_documentation_for_project_per_folder(
        project=output_project, project_name=project_name, output_logger=output_logger)
    output_logger.info("Folders indexed successfully.")

    # Generate indexes
    output_logger.info("Updating indexed data...")
    output_project_for_indexing = ProjectStructure(
        target_path=outputs_absolute_dir+'/'+project_name)
    raw_docs = []
    all_files = output_project_for_indexing.get_all_files(False)
    length_of_all_files = len(all_files)

    for file in all_files:
        abs_folder_path = os.path.join(os.getcwd(), file.path)
        parts = file.path.split("/")

        # Find the index of the first occurrence of "convos"
        # Find the index of the first occurrence of "convos"
        try:
            outputs_index = parts.index(settings.output_folder)
        except ValueError:
            output_logger.error(f"'outputs' not found in path: {file.path}")
            continue  # Skip this file if 'outputs' is not in the path

        # Extract the path from "outputs" and forward
        # 1 because:
        # 0 would be outputs
        # 1 would be outputs/project_name
        # Extract the path from "outputs" and forward

        rel_path = "/".join(parts[outputs_index+1:])
        raw_docs.append(
            {"abs_path": settings.output_folder+'/'+project_name+'/'+file.path, "path": rel_path, "content": file.get_content(abs_folder_path)})
    embeed_md_files_to_store(project_id, repository_id, raw_docs,
                             files_map, user['id'], process_id)

    output_logger.info("Indexed data successfully updated.")
    output_logger.info("Process finished.")
    output_logger.removeHandler(logger)
    return length_of_all_files


#########
# Helpers
#########
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


def _read_content_from_path(absolute_path):
    with open(absolute_path, 'r') as file:
        return file.read()


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


#########
# Subsequent tasks!
# Tasks made for processing fales
#########
# def generate_documentation_for_project_per_file(project: ProjectStructure, project_name='', output_logger: logging = None):
#     all_files = project.get_all_files(keep_root_files=False)
#     current_dir = Path(os.getcwd())

#     for file in all_files:
#         try:
#             if (output_logger is not None):
#                 output_logger.info(f'Processing file: {file.entry}')
#             print(f'Now processing file: ${file.entry}')
#             temp_file_path = Path(file.absolute_path)
#             file_extension = temp_file_path.suffix[1:]  # remove the dot
#             print('lol')
#             result_path = current_dir.joinpath(temp_file_path.parent)
#             result_path_str = str(result_path)

#             result_path_str = result_path_str.replace(
#                 settings.temp_folder+'/'+project_name, settings.output_folder+'/'+project_name)

#             save_name_format = f"{temp_file_path.stem}.{file_extension}"
#             finish_file_ext = 'md'
#             if not save_name_format.endswith('.'):
#                 finish_file_ext = '.md'
#             save_name_format = f"{save_name_format}{finish_file_ext}"
#             error = None
#             if temp_file_path.name.endswith('package.json'):
#                 _, error = get_gpt_response_from_template(
#                     data=get_package_json_data(file.absolute_path), template='parse_package_json', trim_content=True, save_to_subfolder=result_path_str, save_to_name=save_name_format, ignore_output_folder_on_save=True)
#                 if not error:
#                     _, error = get_gpt_response_from_template(
#                         data=get_package_json_data_for_dependencies(file.absolute_path), template='parse_package_json_dependencies', trim_content=True, save_to_subfolder=result_path_str, save_to_name=temp_file_path.stem + '_dependencies' + '.md', ignore_output_folder_on_save=True)
#             elif file_extension in list_of_accepted_docs_file_extensions:
#                 _, error = get_gpt_response_from_template(
#                     data={'file_name': file.name}, template='parse_document_file', trim_content=True, trim_path=file.absolute_path, save_to_subfolder=result_path_str, save_to_name=save_name_format, ignore_output_folder_on_save=True)
#             else:
#                 _, error = get_gpt_response_from_template(
#                     data={'file_name': file.name}, template='document_file_prompt', trim_content=True, trim_path=file.absolute_path, save_to_subfolder=result_path_str, save_to_name=save_name_format, ignore_output_folder_on_save=True)
#             if error:
#                 if (output_logger is not None):
#                     output_logger.error(
#                         'Error on catched calls from openai', error)
#                 print('Error on generating', error)
#         except Exception as e:
#             print('Error on calls from openai', error)
#             if (output_logger is not None):
#                 output_logger.error(
#                     'Error on calls from openai fatal exception', error)


def process_file(file, project_name, output_logger):
    current_dir = Path(os.getcwd())
    try:
        if (output_logger is not None):
            output_logger.info(f'Processing file: {file.entry}')
        print(f'Now processing file: ${file.entry}')
        temp_file_path = Path(file.absolute_path)
        file_extension = temp_file_path.suffix[1:]  # remove the dot
        print('lol')
        result_path = current_dir.joinpath(temp_file_path.parent)
        result_path_str = str(result_path)

        result_path_str = result_path_str.replace(
            settings.temp_folder+'/'+project_name, settings.output_folder+'/'+project_name)

        save_name_format = f"{temp_file_path.stem}.{file_extension}"
        finish_file_ext = 'md'
        if not save_name_format.endswith('.'):
            finish_file_ext = '.md'
        save_name_format = f"{save_name_format}{finish_file_ext}"
        error = None
        if temp_file_path.name.endswith('package.json'):
            _, error = get_gpt_response_from_template(
                data=get_package_json_data(file.absolute_path), template='parse_package_json', trim_content=True, save_to_subfolder=result_path_str, save_to_name=save_name_format, ignore_output_folder_on_save=True)
            if not error:
                _, error = get_gpt_response_from_template(
                    data=get_package_json_data_for_dependencies(file.absolute_path), template='parse_package_json_dependencies', trim_content=True, save_to_subfolder=result_path_str, save_to_name=temp_file_path.stem + '_dependencies' + '.md', ignore_output_folder_on_save=True)
        elif file_extension in list_of_accepted_docs_file_extensions:
            _, error = get_gpt_response_from_template(
                data={'file_name': file.name}, template='parse_document_file', trim_content=True, trim_path=file.absolute_path, save_to_subfolder=result_path_str, save_to_name=save_name_format, ignore_output_folder_on_save=True)
        else:
            _, error = get_gpt_response_from_template(
                data={'file_name': file.name}, template='document_file_prompt', trim_content=True, trim_path=file.absolute_path, save_to_subfolder=result_path_str, save_to_name=save_name_format, ignore_output_folder_on_save=True)
        if error:
            if (output_logger is not None):
                output_logger.error(
                    'Error on catched calls from openai', error)
            print('Error on generating', error)
    except Exception as e:
        print('Error on calls from openai', error)
        if (output_logger is not None):
            output_logger.error(
                'Error on calls from openai fatal exception')


def generate_documentation_for_project_per_folder(project: ProjectStructure, project_name='', output_logger: logging = None):
    all_folders = project.get_all_folders()
    all_folders.reverse()
    root_path = Path(f"{settings.output_folder}/{project_name}")
    for folder in all_folders:
        print(f'Now processing folder: ${folder.path}')
        if (output_logger is not None):
            output_logger.info(f'Processing folder: {folder.path}')
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
        _, error = get_gpt_response_from_template(
            data={'mdFileName': folder.name, 'trimmable_content': query_content}, template='parse_folder_document', trim_content=True, save_to_subfolder=folder.path, save_to_name=folder.name + '.md', ignore_output_folder_on_save=True)
        if error:
            print('Error on calls from openai in folders processing')
            if (output_logger is not None):
                output_logger.error(
                    'Error on calls from openai in folders processing')


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


def record_stripe_files(payload):
    url = settings.MONOLITH_URL + "/api/stripe/sync-files-credits"
    # Make the POST request
    response = requests.post(url, json=payload)

    # Check the response
    if response.ok:
        print("Request successful.")
        print("Response:", response.text)
    else:
        print("Request failed.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

# @celery.task(bind=True)
# self,


@celery.task()
def index_project_files(id_user, repository, id_project, process):
    print('=================')
    print('=================')
    print(id_user)
    print(id_user)
    print(id_user)
    print(id_user)
    print(id_user)
    print(id_user)
    print(json.dumps(repository, separators=(',', ':')))
    # self.update_state(state='STARTED')
    id_repository = repository['id']
    is_github_repo = repository['repositoryType'] == "github"
    if not os.path.exists(temp_absolute_dir):
        os.makedirs(temp_absolute_dir)
    initialization_output_logger = Logger()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    initialization_output_logger.setFormatter(formatter)
    try:
        user = get_user(id_user).data
        processed_files = 0
        if is_github_repo:
            repoOrgName = repository['repoOrganizationName']
            repoName = repository['repoProjectName']
            project_name = f'{repoOrgName}|{repoName}'

            if not os.path.exists(temp_absolute_dir + '/' + project_name):
                os.makedirs(temp_absolute_dir + '/' + project_name)
            if not os.path.exists(outputs_absolute_dir + '/' + project_name):
                os.makedirs(outputs_absolute_dir + '/' + project_name)
            processed_files = process_github_repository(
                process['id'], initialization_output_logger, project_name, repository, user[0], repoOrgName, repoName, id_project)
        else:
            project_name = id_repository
            print('BEFORE ENTERING get_unsynced_repository_docs',)
            db_repo_docs = get_unsynced_repository_docs(id_repository).data
            print('BEFORE ENTERING save_db_docs_to_temp_folder',)
            files_map = save_db_docs_to_temp_folder(
                initialization_output_logger, db_repo_docs, project_name)
            print('passed save_db_docs_to_temp_folder',)

            if not os.path.exists(temp_absolute_dir + '/' + project_name):
                os.makedirs(temp_absolute_dir + '/' + project_name)
            if not os.path.exists(outputs_absolute_dir + '/' + project_name):
                os.makedirs(outputs_absolute_dir + '/' + project_name)
            processed_files = process_normal_repository(
                process['id'], user[0], repository['id'], initialization_output_logger, project_name, files_map, id_project)

        logs = initialization_output_logger.get_logs()
        update_process_end_date_and_logs(process['id'], logs)
        orgResponse = get_project_by_id(id_project)
        print(orgResponse.data)

        payload = {
            "quantity": processed_files,
            "orgId": orgResponse.data[0]['organizationId']
        }
        if processed_files > 0:
            record_stripe_files(payload)
    except Exception as e:
        traceback.print_exc()  # This prints the full traceback
        # You can also log the exception message if needed
        print('Fatal on index project files', str(e))
    # Delete created temp & output folder
    if os.path.exists(temp_absolute_dir + '/' + project_name):
        shutil.rmtree(temp_absolute_dir + '/' + project_name)
    if os.path.exists(outputs_absolute_dir + '/' + project_name):
        shutil.rmtree(outputs_absolute_dir + '/' + project_name)
   # self.update_state(state='FINISHED')

    return 'FINISHED'
