from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
import os
import json
import pandas as pd
import numpy as np

from src.recommendation_functions.combined_recommendations import get_combined_recommendations
from src.recommendation_functions.recommendations_user import get_ratings


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

dataset = pd.read_csv(os.path.join(os.path.dirname(__file__).replace('server','data'), 'datasets/movielens_1M.csv'))
nratings = len(dataset)

links = {}
user_link_list = []

# Check if the JSON file exists, and create it if it doesn't
if not os.path.exists('./users.json'):
    with open('./users.json', 'w') as user_file:
        json.dump({"users": []}, user_file)

# Load user data from the JSON file
with open('./users.json', 'r') as user_file:
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

    #Here we create the link
    while True:
        random = np.random.randint(nratings)
        user_id_link = dataset['user_id'][random]
        if user_id_link not in user_link_list:
            user_link_list.append(user_id_link)
            links[reg_username] = user_id_link
            break

    # Save the updated user data to the JSON file
    with open('./users.json', 'w') as user_file:
        json.dump(user_data, user_file, indent=2)
    
    #

    print (links)

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
    username = session['username']
    print (username)
    top_1user = recommendations(links[username])
    avg_ratings = ratings_dataset(dataset)
    return render_template('hello.html', data=df, top5=top_1user, avg = avg_ratings)#.to_dict(orient='records'), top5=top_1user)

@app.route('/', methods=['GET', 'POST'])
def combined_recommendations(user1_id, user2_id, n=5, c=0.5):
    comb_rec = get_combined_recommendations(user1_id, user2_id, n, c)
    return jsonify({'top_recommendations': comb_rec})

@app.route('/', methods=['GET', 'POST'])
def recommendations(user1_id, top=5):
    _,rec = get_ratings(user = user1_id)
    return rec
    #return jsonify({'top_recommendations': rec})

@app.route('/', methods=['POST'])
def ratings_dataset(data):
    avg_ratings = {}
    for id in np.unique(data['item_id']):
        aux = dataset[data['item_id']==id]
        avg_ratings[id] = round (np.mean(aux['rating']),1)
    return avg_ratings

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