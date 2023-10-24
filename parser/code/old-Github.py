import requests

GITHUB_API_URL = "https://api.github.com"


# def get_latest_synced_commit(repository_id: str) -> str:
#     documents = get_unsynced_repository_docs(repository_id)
#     if not documents:
#         return None
#     return documents[0]['latest_sync_date']


# def get_commits_since_last_synced(owner: str, repo: str, since_sha: str) -> list:
#     headers = {
#         "Authorization": f"token {settings.GITHUB_TOKEN}",
#         "Accept": "application/vnd.github.v3+json"
#     }
#     commits_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits"
#     params = {
#         "since": since_sha
#     }
#     response = requests.get(commits_url, headers=headers, params=params)
#     return response.json()


# def get_commit_files(owner: str, repo: str, sha: str) -> dict:
#     headers = {
#         "Authorization": f"token {settings.GITHUB_TOKEN}",
#         "Accept": "application/vnd.github.v3+json"
#     }
#     commit_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits/{sha}"
#     response = requests.get(commit_url, headers=headers)
#     commit_data = response.json()
#     added_files = [file['filename']
#                    for file in commit_data['files'] if file['status'] == 'added']
#     removed_files = [file['filename']
#                      for file in commit_data['files'] if file['status'] == 'removed']
#     return {
#         'added': added_files,
#         'removed': removed_files
#     }


# def get_update_documents_from_commits(repository_id: str, owner: str, repo: str):
#     # Get the latest synced commit
#     latest_synced_commit = get_latest_synced_commit(repository_id)
#     if not latest_synced_commit:
#         print("No synced commit found.")
#         return

#     # Get all commits since the latest synced commit
#     commits = get_commits_since_last_synced(owner, repo, latest_synced_commit)

#     all_added_files = []
#     all_removed_files = []

#     for commit in commits:
#         commit_files = get_commit_files(owner, repo, commit['sha'])
#         all_added_files.extend(commit_files['added'])
#         all_removed_files.extend(commit_files['removed'])

#     return all_added_files, all_removed_files


# Usage
# Assuming you have 'owner' and 'repo' details
# added_files, removed_files = update_documents_from_commits(
#     "YOUR_REPOSITORY_ID", "GITHUB_OWNER", "GITHUB_REPO_NAME")
# print("Added files:", added_files)
# print("Removed files:", removed_files)
