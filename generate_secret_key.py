import secrets

# Génère une clé secrète de 32 octets (256 bits)
secret_key = secrets.token_hex(32)

print("Generated secret key:")
print(secret_key)
