from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Implement endpoint
@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    conn = sqlite3.connect('totally_not_my_privateKeys.db')
    cursor = conn.cursor()

    cursor.execute("SELECT key FROM keys WHERE exp > ?", (datetime.now().timestamp(),))
    keys = cursor.fetchall()
    jwks_data = {"keys": [key[0].decode('utf-8') for key in keys]}

    conn.close()

    return jsonify(jwks_data)

if __name__ == '__main__':
    app.run(debug=True)
