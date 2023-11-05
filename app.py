from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# A simple user database for demonstration
users = {'user': 'password'}

# Define a login route
@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('hello'))
        else:
            return "Invalid login"

    return render_template('main.html')  # Update the template name here

# Define the registration route
@app.route('/register', methods=['POST'])
def register():
    reg_username = request.form['reg_username']
    reg_password = request.form['reg_password']
    
    # Here, you can save the registration data to your user database or perform any desired actions.
    # For simplicity, we'll just print the data for demonstration.
    print(f"Registered: Username - {reg_username}, Password - {reg_password}")
    
    return "Registration successful"


# Define a "Hello, World!" route
@app.route('/hello')
def hello():
    if 'username' in session:
        return f"Hello, {session['username']}! This is the 'Hello, World!' page."
    return "You are not logged in."

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
