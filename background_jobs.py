from parser.file.ProjectStructure import ProjectStructure
from parser.file.FolderStructure import FolderStructure
from parser.code.ParseCode import generate_root_config_files, generate_documentation_for_project_per_file, generate_documentation_for_project_per_folder
from parser.code.RepoHandling import clone_repo_to_folder
from llm.open_ai import get_gpt_response_from_template
from config.settings import settings
import json
from llm.embeeding import embeed_md_files_to_store, embeed_github_files_to_store
from llm.tokens import group_and_partition_documents
from persister.supabase import update_process_end_date_and_logs, insert_process, get_user, get_unsynced_repository_docs
from logger.Logger import Logger
import logging
import os
import shutil
from celery import Celery
from celery.result import AsyncResult
# from parser.code.base import transform_to_docs
# from parser.code.javascript import extract_functions_and_classes
# from parser.DirectoryIterator import DirectoryIterator
# from celery.utils.log import get_task_logger
from llm.tokens import group_and_partition_documents
from parser.file.ProjectStructure import ProjectStructure
from config.settings import settings
from datetime import datetime


celery = Celery()
celery.config_from_object("config.celery_config")
temp_absolute_dir = os.path.join(os.getcwd(), settings.temp_folder)
outputs_absolute_dir = os.path.join(os.getcwd(), settings.output_folder)


def get_process_status(process_id):
    process = AsyncResult(process_id)

    return {"status": process.status, "details": process.info}


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


def process_github_repository(process_id, logger, project_name, repository, user, repoOrgName, repoName):
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
    generate_documentation_for_project_per_file(
        project=project, project_name=project_name, output_logger=output_logger)
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

    for file in all_files:
        abs_folder_path = os.path.join(os.getcwd(), file.path)
        parts = file.path.split("/")

        # Find the index of the first occurrence of "convos"
        convos_index = parts.index("convos")

        # Extract the path from "outputs" and forward
        # 3 because:
        # 0 would be convos
        # 1 would be convos/outputs
        # 2 would be convos/outputs/project_name
        # 3 would be convos/outputs/project_name/...
        rel_path = "/".join(parts[convos_index+3:])
        raw_docs.append(
            {"abs_path": settings.output_folder+'/'+project_name+'/'+file.path, "path": rel_path, "content": file.get_content(abs_folder_path)})
    embeed_github_files_to_store(
        repository, project_name, user['id'], process_id)

    output_logger.info("Indexed data successfully updated.")
    output_logger.info("Process finished.")

    # Delete created temp & output folder
    # if os.path.exists(temp_absolute_dir + '/' + project_name):
    #     shutil.rmtree(temp_absolute_dir + '/' + project_name)
    # if os.path.exists(outputs_absolute_dir + '/' + project_name):
    #     shutil.rmtree(outputs_absolute_dir + '/' + project_name)
    # self.update_state(state='FINISHED')
    output_logger.removeHandler(logger)


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
    generate_documentation_for_project_per_file(
        project=project, project_name=project_name, output_logger=output_logger)
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

    for file in all_files:
        abs_folder_path = os.path.join(os.getcwd(), file.path)
        parts = file.path.split("/")

        # Find the index of the first occurrence of "convos"
        convos_index = parts.index("convos")

        # Extract the path from "outputs" and forward
        # 3 because:
        # 0 would be convos
        # 1 would be convos/outputs
        # 2 would be convos/outputs/project_name
        # 3 would be convos/outputs/project_name/...
        rel_path = "/".join(parts[convos_index+3:])
        raw_docs.append(
            {"abs_path": settings.output_folder+'/'+project_name+'/'+file.path, "path": rel_path, "content": file.get_content(abs_folder_path)})
    embeed_md_files_to_store(project_id, repository_id, raw_docs,
                             files_map, user['id'], process_id)

    output_logger.info("Indexed data successfully updated.")
    output_logger.info("Process finished.")
    output_logger.removeHandler(logger)


@celery.task(bind=True)
def index_project_files(self, id_user, repository):
    self.update_state(state='STARTED')
    id_repository = repository['id']
    # id_project = repository['projectId']
    is_github_repo = repository['repositoryType'] == "github"

    if not os.path.exists(temp_absolute_dir):
        os.makedirs(temp_absolute_dir)
    initialization_output_logger = Logger()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    initialization_output_logger.setFormatter(formatter)
    # Pull data
    process = insert_process(
        repository['projectId'], id_repository, datetime.now().isoformat())
    try:
        user = get_user(id_user).data
        if is_github_repo:
            repoOrgName = repository['repoOrganizationName']
            repoName = repository['repoProjectName']
            project_name = f'{repoOrgName}|{repoName}'

            if not os.path.exists(temp_absolute_dir + '/' + project_name):
                os.makedirs(temp_absolute_dir + '/' + project_name)
            if not os.path.exists(outputs_absolute_dir + '/' + project_name):
                os.makedirs(outputs_absolute_dir + '/' + project_name)
            process_github_repository(
                process['id'], initialization_output_logger, project_name, repository, user[0], repoOrgName, repoName)
        else:
            project_name = id_repository
            db_repo_docs = get_unsynced_repository_docs(id_repository).data
            files_map = save_db_docs_to_temp_folder(
                initialization_output_logger, db_repo_docs, project_name)

            if not os.path.exists(temp_absolute_dir + '/' + project_name):
                os.makedirs(temp_absolute_dir + '/' + project_name)
            if not os.path.exists(outputs_absolute_dir + '/' + project_name):
                os.makedirs(outputs_absolute_dir + '/' + project_name)
            process_normal_repository(
                process['id'], user[0], repository['id'], initialization_output_logger, project_name, files_map, repository['projectId'])
    except Exception as e:
        print(e)
        print(e)
        print(f'Error: {e}')
    logs = initialization_output_logger.get_logs()
    update_process_end_date_and_logs(process['id'], logs)

    # Delete created temp & output folder
    if os.path.exists(temp_absolute_dir + '/' + project_name):
        shutil.rmtree(temp_absolute_dir + '/' + project_name)
    if os.path.exists(outputs_absolute_dir + '/' + project_name):
        shutil.rmtree(outputs_absolute_dir + '/' + project_name)
    self.update_state(state='FINISHED')

    return 'FINISHED'


# logger = get_task_logger(__name__)

 # return {"status": process.status, "details": process.info}


# def get_metadata_from_filename(title):
#     return {'title': title}


# ['.js', '.md', '.ts', '.tsx', '.jsx', ],
# @celery.task(bind=True)
# def index_project_files(self):
#     print(celery.autodiscover_tasks())
#     self.update_state(state='STARTING')
#     # full_path = 'temp'  # ,./outputs'

#     # reader_params = {
#     #     'input_dir': full_path,
#     #     'input_files': None,
#     #     'recursive': True,
#     #     'required_exts': ['.md'],  # ['.js'],
#     #     'num_files_limit': None,
#     #     'exclude_hidden': True,
#     #     'file_metadata': get_metadata_from_filename
#     # }

#     # functions_dict, classes_dict = extract_functions_and_classes(
#     #    './temp/test-code')
#     # transform_to_docs(functions_dict, classes_dict, './temp/test-code')
#     # raw_docs = DirectoryIterator(**reader_params).load_data()
#    # Generate documentation for all folders
#     project_name = '0xpasho|codesapiens'
#     output_project = ProjectStructure(
#         target_path=settings.output_folder+'/'+project_name)
#     all_files = output_project.get_all_files()
#     self.update_state(state='PROGRESS')
#     raw_docs = []
#     for file in all_files:
#         raw_docs.append(file.get_content(file.path))
#     raw_docs_v2 = group_and_partition_documents(documents=raw_docs)
#     parsed_docs = [Document.to_langchain_format(
#         raw_doc) for raw_doc in raw_docs_v2]
#     embeed_md_files_to_store(docs=parsed_docs)

#     self.update_state(state='FINISHED')

#     return {"status": "FINISHED"}
