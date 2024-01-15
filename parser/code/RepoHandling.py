import jwt
import requests
import time
import subprocess
import os
from config.settings import settings
import shutil
from git import Repo
import base64

# Constants
APP_ID = settings.GITHUB_APP_ID_NUMBER  # GitHub App ID
# Path to your GitHub App's private key
PRIVATE_KEY_PATH = 'github-app-private-key.pem'
GITHUB_API_URL = 'https://api.github.com/'


def generate_jwt():
    """Generate JWT for GitHub App."""
    private_key_encoded = settings.GITHUB_APP_PRIVATE_KEY_BASE64
    if not private_key_encoded:
        raise ValueError(
            f"The environment variable 'GITHUB_APP_PRIVATE_KEY_BASE64' is not set")
    private_key = base64.b64decode(private_key_encoded)
    # Create JWT token which is valid for 10 minutes
    payload = {
        'iat': int(time.time()),
        'exp': int(time.time()) + (10 * 60),
        'iss': APP_ID
    }
    return jwt.encode(payload, private_key, algorithm='RS256')


def get_installation_access_token(installation_id):
    """Get installation access token for a GitHub App installation."""
    jwt_token = generate_jwt()
    print("the installation id", installation_id)
    print("the installation id", installation_id)
    print("the installation id", installation_id)
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.post(
        f'https://api.github.com/app/installations/{installation_id}/access_tokens',
        headers=headers
    )

    if response.status_code != 200:
        # Log the error details and return None or raise a custom exception
        # You can log response.text or response.json() based on the API's error message format
        print(
            f"Error fetching installation access token: {response.status_code} - {response.text}")
        return None

    response_data = response.json()
    return response_data.get('token')


def clone_repo_to_folder(installation_id, folder_path, org_name, repo_name):
    """Clone a specific repo using a GitHub App's installation access token."""
    folder_path = os.path.join(settings.temp_folder, folder_path)
    access_token = get_installation_access_token(installation_id)
    repo_url = f'https://x-access-token:{access_token}@github.com/{org_name}/{repo_name}.git'
    Repo.clone_from(repo_url, folder_path)
    shutil.rmtree(os.path.join(folder_path, ".git"))
