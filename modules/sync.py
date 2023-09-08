from flask import jsonify
from modules.owncloud_api import create_owncloud_user, get_owncloud_users, user_exists_in_owncloud, update_owncloud_user, delete_owncloud_user
from modules.error_handling import handle_sync_error
from modules.models import db, User
import base64
import requests
from config import ADMIN_CREDENTIALS, OWNCLOUD_API_URL

def sync_users():
    try:
        users = User.query.all()
        for user in users:
            username = user.username
            if user_exists_in_owncloud(username):
                # User exists in both database and OwnCloud, check for updates
                owncloud_user_data = {
                    "userid": username,
                    "password": "password",  # You can set the default password here
                    "groups": ["Everyone"]
                }
                headers = {
                    "Authorization": "Basic " + base64.b64encode(ADMIN_CREDENTIALS.encode()).decode()
                }
                response = update_owncloud_user(username, owncloud_user_data, headers)
                if not response.ok:
                    return jsonify({"error": f"Failed to update user {username} in OwnCloud. Status code: {response.status_code}"}), 500
            else:
                # User exists in database but not in OwnCloud, create user
                user_data = {
                    "userid": username,
                    "password": "password",  # You can set the default password here
                    "groups": ["Everyone"]
                }
                headers = {
                    "Authorization": "Basic " + base64.b64encode(ADMIN_CREDENTIALS.encode()).decode()
                }
                response = create_owncloud_user(user_data, headers)
                if not response.ok:
                    return jsonify({"error": f"Failed to create user {username} in OwnCloud. Status code: {response.status_code}"}), 500

        # Check for deleted users in OwnCloud and delete them
        owncloud_users = get_owncloud_users()
        for owncloud_user in owncloud_users:
            if not User.query.filter_by(username=owncloud_user["userid"]).first():
                response = delete_owncloud_user(owncloud_user["userid"])
                if not response.ok:
                    return jsonify({"error": f"Failed to delete user {owncloud_user['userid']} from OwnCloud. Status code: {response.status_code}"}), 500

        return jsonify({"message": "Synchronization completed successfully!"}), 200
    except Exception as e:
        return handle_sync_error(f"An error occurred during synchronization: {str(e)}"), 500
