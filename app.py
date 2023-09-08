from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache  # Importez Cache depuis flask_caching
import sqlite3
from modules.sync import sync_users
from modules.user_management import delete_user, register_user, update_user

app = Flask(__name__)

# Configuration de CORS
CORS(
    app,
    resources={
        r"/*": {
            "origins": "http://localhost:3000",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type"],
        }
    },
)

# Créer une instance de Limiter
limiter = Limiter(app)

# Configuration de la base de données SQLite OwnCloud
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Désactive le suivi des modifications

# Initialisation de la base de données SQLAlchemy
db = SQLAlchemy(app)

# Initialisation de l'extension Cache
cache = Cache(config={"CACHE_TYPE": "simple"})  # Utilisez un cache simple pour l'exemple, configurez-le selon vos besoins
cache.init_app(app)

# Modèle SQLAlchemy pour la table OwnCloud Users
class OwnCloudUser(db.Model):
    __tablename__ = "oc_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    # Ajoutez d'autres colonnes de la table oc_users si nécessaire

    def __init__(self, username):
        self.username = username

# Route pour vérifier le fonctionnement de l'application
@app.route('/')
def check_app():
    return " Bienvenue sur votre Micro-service Gestion des utilisateurs !"

# Redirection vers OwnCloud
@app.route('/redirect-to-owncloud', methods=['GET'])
def redirect_to_owncloud():
    # Redirige le trafic vers l'URL du service OwnCloud
    return redirect('http://owncloud:8080', code=302)

# Route d'enregistrement d'utilisateur
@app.route('/register', methods=['POST'])
@limiter.limit("5 per minute")  # Limite à 5 requêtes par minute
def register_user_route():
    # Utilisez directement la réponse de la fonction register_user() sans affecter à response et status_code
    response, status_code = register_user()

    if status_code == 201:
        user_id = response.get("user_id")
        access_token = response.get("access_token")
        response_data = {
            "message": response.get("message"),
            "user_id": user_id,
            "access_token": access_token
        }
        return jsonify(response_data), status_code
    else:
        return response, status_code

# Route de synchronisation des utilisateurs
@app.route('/sync', methods=['GET'])
def sync_users_route():
    # Essayer de récupérer les données du cache
    cached_data = cache.get('sync_users_data')

    if cached_data is not None:
        # Si les données sont dans le cache, les retourner
        return jsonify(cached_data)
    else:
        # Si les données ne sont pas dans le cache, exécuter la synchronisation
        response, status_code = sync_users()

        # Mettre les données en cache avec une durée de vie de 60 secondes
        if status_code == 200:
            cache.set('sync_users_data', response, timeout=60)

        return response, status_code

# Route de suppression d'utilisateur
@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    return delete_user(user_id)

# Route de mise à jour d'utilisateur
@app.route('/update/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    new_username = request.form.get('new_username')
    new_password = request.form.get('new_password')
    response, status_code = update_user(user_id, new_username, new_password)
    return response, status_code

# Route pour obtenir la liste des utilisateurs
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = sqlite3.connect('/var/www/html/data_db/owncloud.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM oc_users")
        users = cursor.fetchall()
        conn.close()
        user_list = [{"username": user[0]} for user in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
