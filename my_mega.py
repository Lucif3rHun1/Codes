from flask import Flask, request, jsonify
from mega import Mega

app = Flask(__name__)

mega = Mega()

@app.route('/mega', methods=['POST'])
def mega_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        # Return error message if email or password is missing
        return jsonify({'status': 'error', 'message': 'Email and password are required.'}), 400

    # Login to Mega with email and password
    try:
        mega.login(email, password)
    except Exception as e:
        # Return error message if login failed
        return jsonify({'status': 'error', 'message': str(e)}), 401

    # Get quota information for logged in user
    try:
        quota_info = mega.get_quota()
        used_storage = quota_info['used']
        total_storage = quota_info['total']
    except Exception as e:
        # Return error message if quota information cannot be retrieved
        return jsonify({'status': 'error', 'message': str(e)}), 500

    # Return storage quota information if login successful
    return jsonify({'status': 'success', 'used_storage': used_storage, 'total_storage': total_storage}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
