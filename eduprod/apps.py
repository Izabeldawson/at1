from django.apps import AppConfig


class EduprodConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eduprod'

from http.server import BaseHTTPRequestHandler, HTTPServer
import hashlib
import http.cookies
import os

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
    token = hashlib.sha256(os.urandom(64)).hexdigest()
    response = f'HTTP/1.1 303 See Other\r\nLocation: /dashboard\r\nSet-Cookie: remember_token={token}; Max-Age=604800; Path=/\r\n'
    return response.encode('utf-8')

# Dummy login functionality
def login(username, password):
    if username in users and users[username]['password'] == password:
        return True
    return False

# HTTP request handler
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><form method='post'>Username:<input type='text' name='username'><br>Password:<input type='password' name='password'><br>Remember Me:<input type='checkbox' name='remember_me'><br><input type='submit' value='Login'></form></body></html>")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        username = post_data.split('&')[0].split('=')[1]
        password = post_data.split('&')[1].split('=')[1]
        remember_me = 'remember_me' in post_data

        if login(username, password):
            if remember_me:
                response = set_remember_cookie(username)
            else:
                response = b'HTTP/1.1 303 See Other\r\nLocation: /dashboard\r\n'
        else:
            response = b'HTTP/1.1 401 Unauthorized\r\n\r\nInvalid username or password'

        self.wfile.write(response)

# Main function to run the HTTP server
def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
