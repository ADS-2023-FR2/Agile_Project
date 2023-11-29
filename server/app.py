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

@app.route('/static/<path:filename>')
def serve_css(filename):
    return send_from_directory('static', filename)



# Search and select friends
# ________________________________________________________________________________

# Sample user database (replace this with your actual user data)
users = [
    {"id": 1, "username": "Pol G"},
    {"id": 2, "username": "Pol R"},
    {"id": 3, "username": "David"},
    {"id": 4, "username": "Sergi"},
    {"id": 5, "username": "Joachim"},
    {"id": 6, "username": "Vinny"},
    {"id": 7, "username": "Ana"},
    {"id": 8, "username": "EloiBestTeacher"}
    # Add more users here...
]

@app.route('/hello', methods=['GET'])
def hello():
    return render_template('hello.html')

@app.route('/search', methods=['GET'])
def search_users():
    query = request.args.get('query', '')  # Get search query from request parameters
    results = []
    if query:
        # Simulated search logic (replace with your actual search logic)
        results = [user for user in users if query.lower() in user['username'].lower()]
    return jsonify(results)

@app.route('/save_selected_user', methods=['POST'])
def save_selected_user():
    selected_user = request.get_json()  # Get the selected user data from the request
    
    return jsonify({'message': 'Selected user received successfully'})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
