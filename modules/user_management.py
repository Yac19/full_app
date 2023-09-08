# user_management.py

from flask import request, jsonify
import requests
from modules.owncloud_api import delete_owncloud_user, user_exists_in_owncloud
from modules.error_handling import handle_registration_error
from modules.models import db, User, user_exists
import base64
from config import ADMIN_CREDENTIALS, OWNCLOUD_API_URL, SECRET_KEY
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bcrypt

def generate_token(user_id):
    s = Serializer(SECRET_KEY, expires_in=3600)  # 1 heure d'expiration
    token = s.dumps({'user_id': user_id}).decode('utf-8')
    return token

def register_user():
    # Obtenir les données du formulaire
    username = request.form.get("username")
    password = request.form.get("password")

    if user_exists(username) and user_exists_in_owncloud(username):
        return handle_registration_error("L'utilisateur existe déjà.", 400)

    user_data = {
        "userid": username,
        "password": password,
        "groups": ["Everyone"]
    }

    headers = {
        "Authorization": "Basic " + base64.b64encode(ADMIN_CREDENTIALS.encode()).decode()
    }

    response = requests.post(OWNCLOUD_API_URL, data=user_data, headers=headers)

    if response.ok:
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()

        # Générer un jeton d'accès pour l'utilisateur nouvellement enregistré
        token = generate_token(new_user.id)

        return {
            "message": "Utilisateur enregistré avec succès !",
            "access_token": token,
            "user_id": new_user.id  # Ajout de l'ID utilisateur dans la réponse
        }, 201
    else:
        return handle_registration_error(f"Échec de l'enregistrement de l'utilisateur. Code de statut : {response.status_code}", 500)

def update_user(user_id, new_username, new_password):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    if user_exists(new_username):
        return jsonify({"error": "Le nom d'utilisateur existe déjà."}), 400

    user.username = new_username
    user.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    db.session.commit()

    return jsonify({"message": "Utilisateur mis à jour avec succès !"}), 200

def delete_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    # Supprimer l'utilisateur de votre base de données
    db.session.delete(user)
    db.session.commit()

    # Appeler la fonction pour supprimer l'utilisateur d'OwnCloud
    response_owncloud = delete_owncloud_user(user.username)
    if not response_owncloud.ok:
        return jsonify({"error": f"Échec de la suppression de l'utilisateur {user.username} d'OwnCloud. Code de statut : {response_owncloud.status_code}"}), 500

    return jsonify({"message": "Utilisateur supprimé avec succès !"}), 200
