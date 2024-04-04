from django.apps import AppConfig


class EduprodConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eduprod'
from flask import Flask, request, make_response, redirect, render_template
import hashlib
import uuid

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Dummy user database (replace with your actual user database)
users = {
    'user1': {
        'username': 'user1',
        'password': 'password1'
    },
    'user2': {
        'username': 'user2',
        'password': 'password2'
    }
}

# Function to generate and set a remember me token
def set_remember_cookie(username):
    token = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    response = make_response(redirect('/'))
    response.set_cookie('remember_token', token, max_age=604800)  # Set cookie to expire in 7 days
    return response

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = request.form.get('remember_me')  # Check if 'Remember Me' checkbox is checked

        if username in users and users[username]['password'] == password:
            if remember_me:
                # If 'Remember Me' checkbox is checked, set a remember me token
                return set_remember_cookie(username)
            else:
                # If 'Remember Me' checkbox is not checked, set a session cookie
                return redirect('/')
        else:
            return 'Invalid username or password'

    return render_template('login.html')

# Homepage route
@app.route('/')
def home():
    if 'remember_token' in request.cookies:
        # Check if remember token exists, if yes, auto login the user
        token = request.cookies.get('remember_token')
        # Here you would validate the token and perform necessary actions to log in the user
        return f'You are logged in using remember me feature!'
    return 'You are not logged in.'

if __name__ == '__main__':
    app.run(debug=True)
