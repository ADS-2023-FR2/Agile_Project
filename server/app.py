from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
import os
import json
import pandas as pd

from src.recommendation_functions.combined_recommendations import get_combined_recommendations


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Sample movie data (replace this with your actual recommendation logic)
top_movies = [
    {'title': 'Movie 1', 'genre': 'Action'},
    {'title': 'Movie 2', 'genre': 'Drama'},
    {'title': 'Movie 3', 'genre': 'Comedy'},
    {'title': 'Movie 4', 'genre': 'Sci-Fi'},
    {'title': 'Movie 5', 'genre': 'Thriller'}
]

# Read the CSV file using a relative path
df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'images/m1movidata.csv'))

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

@app.route('/hello', methods=['GET'])
def hello():
    #print("hello was called")
    updated_array_str = request.args.get('updatedArray', None)
    if updated_array_str:
        hidden_integer_array = json.loads(updated_array_str)
    else: 
        hidden_integer_array =[11, 20, 30, 40, 50, 11, 20, 30, 40, 50]
    #print("handover recomedations:"+ str(hidden_integer_array))
    sample_user_id = 2
    return render_template('hello.html', data=df.to_dict(orient='records'), hiddenIntegerArray=hidden_integer_array, own_user_id=sample_user_id)

@app.route('/update_array', methods=['POST'])
def update_array():
    updated_array = request.json.get('updatedArray', [])
    print("updated_array" + str(updated_array))
    return 'OK'

@app.route('/combined_recommendations', methods=['GET'])
def combined_recommendations():
    own_user_id = request.args.get('own_user_id')
    friend_user_id = request.args.get('friend_user_id')
    n = 5
    c = 0.5
    #comb_rec = get_combined_recommendations(own_user_id, friend_user_id, n, c)
    comb_rec = [101,102,103,104,105]
    print("userids: " + str(own_user_id) + " / " +str(friend_user_id))
    print(friend_user_id)
    return jsonify(comb_rec)

def load_data_from_csv(csv_file):
    data = {}
    with open(csv_file, 'r') as file:
        for line in file:
            id, link = line.strip().split(',')
            data[id] = link
    return data


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
