from flask import Flask, request, jsonify
from modules.user_management import delete_user, register_user
from modules.sync import sync_users
from modules.models import db

app = Flask(__name__)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactive le suivi des modifications
db.init_app(app)

# Routes
@app.route('/register', methods=['POST'])
def register_user_route():
    response, status_code = register_user()

    # Vérifiez si la requête a été exécutée avec succès
    if status_code == 201:
        # Extrait les informations de la réponse JSON
        user_id = response.get("user_id")
        access_token = response.get("access_token")

        # Crée un nouveau dictionnaire avec les informations nécessaires
        response_data = {
            "message": response.get("message"),
            "user_id": user_id,
            "access_token": access_token
        }

        return jsonify(response_data), status_code
    else:
        return response, status_code

@app.route('/sync', methods=['POST'])
def sync_users_route():
    return sync_users()

@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    return delete_user(user_id)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
