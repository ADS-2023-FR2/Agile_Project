from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Check if the JSON file exists, and create it if it doesn't
if not os.path.exists('users.json'):
    with open('users.json', 'w') as user_file:
        json.dump({"users": []}, user_file)

# Load user data from the JSON file
with open('users.json', 'r') as user_file:
    user_data = json.load(user_file)

# Define a main route
@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('main.html')

# Define the login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['reg_username']
    password = request.form['reg_password']

    for user in user_data['users']:
        if user['username'] == username and user['password'] == password:
            session['username'] = username
            return jsonify({'success': True, 'message': 'Login successful'})
    
    return jsonify({'success': False, 'message': 'Invalid login'})

# Define the registration route
@app.route('/register', methods=['POST'])
def register():
    reg_username = request.form['reg_username']
    reg_password = request.form['reg_password']

    # Append the new user to the user_data list
    user_data['users'].append({
        'username': reg_username,
        'password': reg_password
    })

    # Save the updated user data to the JSON file
    with open('users.json', 'w') as user_file:
        json.dump(user_data, user_file, indent=2)

    return jsonify({'success': True})

@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/static/<path:filename>')
def serve_js(filename):
    return send_from_directory('static', filename)

@app.route('/hello', methods=['GET'])
def hello():
    return render_template('hello.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
