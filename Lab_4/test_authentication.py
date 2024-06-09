from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import unittest

app = Flask(__name__)
app.template_folder = 'my_templates'
app.secret_key = 'supersecretkey'

users = {}  # {'username': 'hashed_password'}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неправильное имя пользователя или пароль!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            users[username] = hashed_password
            flash('Вы успешно зарегистрировались!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Пользователь с таким именем уже существует!', 'danger')
    return render_template('register.html')

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    def test_register_user(self):
        response = self.app.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('Вы успешно зарегистрировались!', str(response.data))
        self.assertIn('messages', response.session)
        self.assertEqual(response.session['messages'][0], 'Вы успешно зарегистрировались!')
    def test_login_user(self):
        self.app.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
        response = self.app.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления
        self.assertIn('Вы успешно вошли в систему!', str(response.data))
        self.assertIn('messages', response.session)
        self.assertEqual(response.session['messages'][0], 'Вы успешно вошли в систему!')

    def test_login_invalid_credentials(self):
        response = self.app.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('messages', response.session)
        self.assertEqual(response.session['messages'][0], 'Неправильное имя пользователя или пароль!')

    def test_register_existing_user(self):
        self.app.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
        response = self.app.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('messages', response.session)
        self.assertEqual(response.session['messages'][0], 'Пользователь с таким именем уже существует!')

if __name__ == '__main__':
    unittest.main()