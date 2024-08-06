from flask import Flask, request, render_template, redirect, url_for, jsonify, flash, session, g
import sqlite3
import os
import uuid
from dotenv import load_dotenv
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import send_from_directory

load_dotenv()

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')  # Change this to a secure key in production

DATABASE = 'manage.db'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM admins WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user is None:
        return None
    return User(id=user['id'], username=user['username'], password=user['password'])

@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        username = request.form['username']
        token = str(uuid.uuid4())

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, token) VALUES (?, ?)", (username, token))
            conn.commit()

            conn = get_db_connection()
            cursor = conn.execute("SELECT username, token FROM users")
            users = cursor.fetchall()
            return render_template('users.html', users=users)
        
        except sqlite3.IntegrityError:
            return 'User already exists or error generating the token.', 400
    
    return render_template('admin.html')


@app.route('/api/data', methods=['GET'])
def protected_data():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token not provided'}), 401

    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM users WHERE token = ?", (token,))
    user_token_ok = cursor.fetchone()
    
    if user_token_ok:
        return jsonify({'data': 'here is the protected data'}), 200
    else:
        return jsonify({'message': 'Invalid token'}), 403

@app.route('/users', methods=['GET'])
@login_required
def list_users():
    conn = get_db_connection()
    cursor = conn.execute("SELECT username, token FROM users")
    users = cursor.fetchall()
    
    return render_template('users.html', users=users)

@app.route('/api/docs', methods=['GET'])
def api_docs():
    return render_template('api_docs.html')


@app.route('/register', methods=('GET', 'POST'))
@login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO admins (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Username already exists.')
            return redirect(url_for('register'))
        finally:
            conn.close()

        flash('User registered successfully.')
        return redirect(url_for('logout'))
    
    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            user_obj = User(id=user['id'], username=user['username'], password=user['password'])
            login_user(user_obj)
            flash('Logged in successfully.')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
