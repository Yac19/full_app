import secrets

# Génère une clé secrète de 32 octets (256 bits)
secret_key = secrets.token_hex(32)

# Écrit la clé secrète dans un fichier nommé "secret_key.txt"
with open("secret_key.txt", "w") as file:
    file.write(secret_key)

print("Clé secrète générée et enregistrée dans secret_key.txt")
