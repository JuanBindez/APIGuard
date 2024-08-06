import argparse
import sqlite3
import getpass
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    conn = get_db_connection()
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                token TEXT UNIQUE NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        print('Database and tables created successfully.')
    finally:
        conn.close()

def register(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO admins (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        print('Superuser created successfully.')
    except sqlite3.IntegrityError:
        print('Error: Username already exists.')
    finally:
        conn.close()

def create_superuser():
    username = input('username > ')
    password = getpass.getpass('password > ')
    register(username, password)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage.py command line interface')
    parser.add_argument('command', help='The command to run')

    args = parser.parse_args()

    if args.command == 'create-superuser':
        create_superuser()
    elif args.command == 'create-database':
        create_database()
    else:
        print(f"Unknown command: {args.command}")
