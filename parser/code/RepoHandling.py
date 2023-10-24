import jwt
import requests
import time
import subprocess
import os
from config.settings import settings
import shutil

# Constants
APP_ID = settings.GITHUB_APP_ID_NUMBER  # GitHub App ID
# Path to your GitHub App's private key
PRIVATE_KEY_PATH = 'github-app-private-key.pem'
GITHUB_API_URL = 'https://api.github.com/'


def can_access_repo(repo_url, installation_token):
    """
    Check if the repository can be accessed with the provided token.
    """
    try:
        # Use ls-remote to check for access without cloning
        result = subprocess.run(['git', 'ls-remote', '-h', repo_url],
                                check=True,
                                capture_output=True,
                                env={'GIT_ASKPASS': 'echo', 'GIT_TERMINAL_PROMPT': '0', 'HOME': os.getcwd()})
    except subprocess.CalledProcessError:
        return False
    return True


def generate_jwt_token(app_id, private_key_path):
    """
    Generate JWT token for GitHub App.
    """

    with open(private_key_path, 'r') as file:
        private_key = file.read()

    # Generate JWT token valid for 10 minutes
    token = jwt.encode({
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),
        "iss": app_id
    }, private_key, algorithm='RS256')
    return token


def get_installation_access_token(installation_id, app_token):
    """
    Get the installation access token for a specific installation ID.
    """
    headers = {
        "Authorization": f"Bearer {app_token}",
        "Accept": "application/vnd.github.machine-man-preview+json"
    }
    response = requests.post(
        f"{GITHUB_API_URL}app/installations/{installation_id}/access_tokens", headers=headers)
    return response.json().get('token')


def clone_specific_repository(installation_token, folder_path, org_name, repo_name):
    """
    Clone a specific repository of the specified organization using the installation token.
    """
    headers = {
        "Authorization": f"token {installation_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    repo_response = requests.get(
        f"{GITHUB_API_URL}repos/{org_name}/{repo_name}", headers=headers)
    repo = repo_response.json()

    # Ensure the repo belongs to the specified organization and has the specified name
    if repo.get('owner', {}).get('login') == org_name and repo.get('name') == repo_name:
        repo_url = repo['clone_url']

        # Pre-check if the repository can be accessed
        if not can_access_repo(repo_url, installation_token):
            print(
                f"Cannot access repository (might require authentication): {repo_name}")
            return

        # Use the git command to clone the repository
        try:
            subprocess.run(['git', 'clone', repo_url, os.path.join(
                settings.temp_folder, folder_path)], check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to clone repository: {repo_name}")
        else:
            print(f"Successfully cloned repository: {repo_name}")
            git_dir_path = os.path.join(
                settings.temp_folder, folder_path, ".git")
            if os.path.exists(git_dir_path):
                shutil.rmtree(git_dir_path)
                print(f"Removed '.git' directory from {repo_name}")


def clone_repo_to_folder(installation_id, folder_path, org_name, repo_name):
    app_token = generate_jwt_token(APP_ID, PRIVATE_KEY_PATH)
    installation_token = get_installation_access_token(
        installation_id, app_token)
    clone_specific_repository(
        installation_token, folder_path, org_name, repo_name)
