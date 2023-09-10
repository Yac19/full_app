#!/bin/sh

# Générer le certificat et la clé privée auto-signés pour localhost
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /certs/localhost.key -out /certs/localhost.crt -subj "/CN=localhost"

# Vous pouvez décommenter les lignes ci-dessous si vous souhaitez démarrer un serveur HTTP simple pour servir les certificats (optionnel)
# Cela peut être utile si vous voulez récupérer les certificats à partir d'un autre conteneur.

# Démarrer un serveur HTTP pour servir les certificats
#openssl s_server -accept 443 -key /certs/localhost.key -cert /certs/localhost.crt -www
