from flask import Flask, request, current_app, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import base64
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os
from flask import request, jsonify
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

app = Flask(__name__)

# Charger les variables d'environnement depuis le fichier .env -> Installer le package via pip install dotenv
load_dotenv()

# Utilisation du caching
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Gestion des taux d'appels avec Flask-Limiter
app.config['REDIS_URL'] = os.getenv('storage__uri')  # URL de votre instance Redis
app.config['REDIS_PREFIX'] = 'flask-limiter-MotDePass:'  # Préfixe pour les clés Flask-Limiter. Lorsque Flask-Limiter stocke des informations dans Redis (par exemple, les limites d'appels par minute ou par jour), il préfixe ces clés avec 'flask-limiter:'.

limiter = Limiter(get_remote_address, app=app, storage_uri=app.config['REDIS_URL'], default_limits=["50 per day", "20 per hour"])


# Utiliser les variables d'environnement
OWNCLOUD_API_URL = os.getenv('OWNCLOUD_API_URL')
admin_credentials = os.getenv('ADMIN_CREDENTIALS')
custom_admin_credentials = os.getenv('admin_credentials')  # Note: Variable names are case-sensitive

# Configurer la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)

# Modèle pour la table des utilisateurs
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100  ), nullable=False)
    
# La route pour mon API sur le port 5000 avec la racine du fichier actuel  
@app.route('/')
def root():
    return '<h2>That\'s my page for my users list</h2>'

@app.route('/users')
def voirUsers():
    all_users = Users.query.all()
#    for user in all_users:
#        print(f"ID: {user.id}, Username: {user.username}, Password: {user.password}")
    # sync_owncloud_users()
    return sync_owncloud_users()

# Changez le type d'argument user_id en string dans la route
@app.route('/update/<string:user_id>', methods=['PUT'])
@limiter.limit("5/minute")
#@cache.memoize(timeout=60)  # Cache pendant 60 secondes
def update_password(user_id):
    #print(request.json.get('new_password'))
    try:
        if user_exists(user_id) and owncloud_user_exists(user_id):  # Vérifiez si l'utilisateur existe
            # print(f"Received request to update password for user: {user_id}")
            user = Users.query.filter_by(username=user_id).first()

            #print(f"Received request to update password for user: {user_id}")

            new_password = request.json.get('new_password')
            #print(f'Nouveau mot de passe_debug1: {new_password}')
            
            group_data = {
                "key": "password",
                "value": new_password
            }

            headers = { 
                "Authorization": "Basic " + base64.b64encode(admin_credentials.encode()).decode()
            }

            response = requests.put(f"{OWNCLOUD_API_URL}/{user_id}", data=group_data, headers=headers)
            
            if response:
                #print(f'Nouveau mot de passe_debug2: {new_password}')
                user.password = new_password # Utilisation de la variable "user" pour la mise à jour
                db.session.commit()  
                return "Mot de passe mis à jour"
            else:
                return "Nouveau mot de passe non fourni", response.status_code
            
        else:
            return "Utilisateur non trouvé", 404
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"Une erreur s'est produite : {str(e)}", 500

# Fonction pour vérifier si un utilisateur existe déjà sur le serveur OwnCloud
def owncloud_user_exists(user_id):
    response = requests.get(OWNCLOUD_API_URL + user_id, auth=tuple(admin_credentials.split(':')))
    return response.status_code

# Fonction pour synchroniser les utilisateurs depuis OwnCloud
def sync_owncloud_users():
    response = requests.get(OWNCLOUD_API_URL.format(userid=""), auth=tuple(admin_credentials.split(':')))
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        user_list = [user.text for user in root.findall(".//data/users/element")]
        users_json = []
        
        for idx, username in enumerate(user_list, start=1):
            existing_user = Users.query.filter_by(username=username).first()
            if existing_user:
                existing_user.username = username
                db.session.merge(existing_user)
            else:
                new_user = Users(username=username, password="default_password")
                db.session.add(new_user)
                db.session.commit()
                
            users_json.append({"ID": idx, "Username": username})
        
        return jsonify(users_json)  # Convertir la liste en JSON et renvoyer

    else:
        print("Erreur lors de la requête GET"), 500

# Fonction pour vérifier si un utilisateur existe déjà dans la base de données locale.
def user_exists(user_id):
    user = Users.query.filter_by(username=user_id).first()
    #print('test user')
    return user is not None

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Créer les tables dans la base de données si elles n'existent pas déjà
        sync_owncloud_users()  # Appeler la fonction pour synchroniser les utilisateurs
        all_users = Users.query.all()
        #for user in all_users:
            #print(f"ID: {user.id}, Username: {user.username}, Password: {user.password}")
    app.run(debug=False, host='173.18.0.6', port=5000)