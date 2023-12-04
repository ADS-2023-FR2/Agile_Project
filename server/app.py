from flask import Flask, render_template, request, jsonify, session, send_from_directory
import os
import json
import pandas as pd
import numpy as np
from random import choice
import pickle

from src.recommendation_functions import combined_recommendations
from src.recommendation_functions.recommendations_user import get_ratings

app = Flask(__name__)
app.secret_key = 'your_secret_key'

dictionary = {}

# Read the CSV file using a relative path
df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'images/m1movidata.csv'))
movielens = pd.read_csv('data/datasets/movielens_1M.csv')

user_list = np.unique(movielens["user_id"])

# Check if the JSON file exists, and create it if it doesn't
if not os.path.exists('server/users.json'):
    with open('server/users.json', 'w') as user_file:
        json.dump({"users": []}, user_file)

# Load user data from the JSON file
with open('server/users.json', 'r') as user_file:
    user_data = json.load(user_file)


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
if not os.path.exists('server/users.json'):
    with open('server/users.json', 'w') as user_file:
        json.dump({"users": []}, user_file)

# Load user data from the JSON file
with open('server/users.json', 'r') as user_file:
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
            user_data['username'] = username
            return jsonify({'success': True, 'message': 'Login successful'})
    
    return jsonify({'success': False, 'message': 'Invalid login'})

# Define the registration route
@app.route('/register', methods=['POST'])
def register():
    reg_username = request.form['reg_username']
    reg_password = request.form['reg_password']

    # Check if the user already exists in the dataset
    matching_user = movielens[movielens['user_id'] == reg_username]

    if not matching_user.empty:
        return jsonify({'success': False, 'message': 'User already exists in the dataset.'})

    # If the user doesn't exist, randomly select an existing user from the dataset
    random_existing_user = choice(movielens['user_id'])
    dictionary["reg_username"] = random_existing_user

    # Associate credentials with the randomly selected user in your database
    # You might want to store reg_password securely (e.g., hash it)
    existing_user_id = random_existing_user
    # Your code to link the user credentials with the randomly selected user

     # Append the new user to the user_data list
    user_data['users'].append({
        'username': reg_username,
        'password': reg_password
    })

    # Save the updated user data to the JSON file
    with open('server/users.json', 'w') as user_file:
        json.dump(user_data, user_file, indent=2)

    # Set the session for the new user
    session['username'] = reg_username
    
    
    # Get recommendations for the newly registered user
    user_recommendations = get_ratings(folder = "src/spotlight", in_model = "models/movielens_1M_model.pkl", in_dataset="data/datasets/movielens_1M.csv", user = existing_user_id, top=5)
    print(user_recommendations)
    # Render the hello.html page with the user recommendations
    return render_template('hello.html', data=user_recommendations)

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
    return render_template('hello.html', data=df.to_dict(orient='records'))

@app.route('/', methods=['GET', 'POST'])
def combined_recommendations(user1_id, user2_id, n=5, c=0.5):
    comb_rec = get_combined_recommendations(user1_id, user2_id, n, c)
    return jsonify({'top_recommendations': comb_rec})

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
