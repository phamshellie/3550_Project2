from flask import Flask, request, jsonify
import sqlite3
import jwt
from datetime import datetime, timedelta

# /auth endpoint
@app.route('/auth', methods=['POST'])
def auth():
    expired = request.args.get('expired')

    conn = sqlite3.connect('totally_not_my_privateKeys.db')
    cursor = conn.cursor()

    if expired:
        cursor.execute("SELECT key FROM keys WHERE exp <= ?", (datetime.now().timestamp(),))
    else:
        cursor.execute("SELECT key FROM keys WHERE exp > ?", (datetime.now().timestamp(),))

    private_key_pem = cursor.fetchone()[0]

    # authentication
    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'userABC' and password == 'password123':
        payload = {'username': username}
        token = jwt.encode(payload, private_key_pem, algorithm='RS256')
        conn.close()
        return jsonify({'token': token.decode('utf-8')})
    else:
        conn.close()
        return jsonify({'message': 'Authentication failed'}), 401
