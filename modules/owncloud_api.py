import base64
import requests
from config import ADMIN_CREDENTIALS, OWNCLOUD_API_URL

def user_exists_in_owncloud(username):
    response = requests.get(f"{OWNCLOUD_API_URL}/{username}", headers={"Authorization": "Basic " + base64.b64encode(ADMIN_CREDENTIALS.encode()).decode()})
    return response.ok

def create_owncloud_user(user_data, headers):
    response = requests.post(OWNCLOUD_API_URL, data=user_data, headers=headers)
    return response

def update_owncloud_user(username, user_data, headers):
    response = requests.put(f"{OWNCLOUD_API_URL}/{username}", data=user_data, headers=headers)
    return response

def delete_owncloud_user(username):
    response = requests.delete(f"{OWNCLOUD_API_URL}/{username}", headers={"Authorization": "Basic " + base64.b64encode(ADMIN_CREDENTIALS.encode()).decode()})
    return response

def get_owncloud_users():
    response = requests.get(OWNCLOUD_API_URL, headers={"Authorization": "Basic " + base64.b64encode(ADMIN_CREDENTIALS.encode()).decode()})
    if response.ok:
        return response.json()
    else:
        return []
