import sqlite3
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta

#generate and save private keys
def generate_and_save_private_key():
    conn = sqlite3.connect('totally_not_my_privateKeys.db')
    cursor = conn.cursor()

    #private key
    private_key = cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Serialize the private key
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    #expiration time for the keys
    current_time = datetime.now()
    expired_time = current_time
    valid_time = current_time + timedelta(hours=1)

    # saving private keys to database
    cursor.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (private_key_pem, expired_time.timestamp()))
    cursor.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (private_key_pem, valid_time.timestamp()))

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Private keys generated and saved successfully.")

generate_and_save_private_key()
