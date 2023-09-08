import unittest
from flask_sqlalchemy import SQLAlchemy
import sys
import os  # Importez le module os

# Ajoutez le répertoire parent au chemin de recherche
sys.path.append("..")

# Importez app et db depuis le répertoire parent
from app import app, db
from modules.models import User
from modules.user_management import register_user, update_user, delete_user


class TestUserManagement(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Créez un contexte d'application Flask
        self.app_context = app.app_context()
        self.app_context.push()

        # Créez les tables de la base de données
        db.create_all()

        # Supprimez l'utilisateur existant s'il y en a un avec le même nom
        existing_user = User.query.filter_by(username='test_user').first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()

    def tearDown(self):
        # Supprimez les tables de la base de données
        db.session.remove()
        db.drop_all()

        # Pop le contexte d'application Flask
        self.app_context.pop()

    def test_register_user(self):
        response = self.app.post('/register', data={'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.json)
        self.assertIn('access_token', response.json)
        self.assertIn('user_id', response.json)

    def test_update_user(self):
        user = User(username='test_user')
        db.session.add(user)
        db.session.commit()

        response = self.app.put(f'/user/{user.id}', data={'new_username': 'new_test_user', 'new_password': 'new_test_password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_delete_user(self):
        user = User(username='test_user')
        db.session.add(user)
        db.session.commit()

        response = self.app.delete(f'/user/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

if __name__ == '__main__':
    unittest.main()
