from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3, hashlib, os

app = Flask(__name__)
CORS(app)

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db.sqlite')
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

def init_db():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    with sqlite3.connect(DB) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
    print("数据库初始化完成")

def hash_pwd(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- 静态资源 ----------
@app.route('/frontend/<path:filename>')
def serve_frontend(filename):
    return send_from_directory(FRONTEND_DIR, filename)

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'contacts.html')

# ---------- 用户 ----------
@app.post('/register')
def register():
    data = request.json
    username, password = data.get('username'), data.get('password')
    if not username or not password:
        return jsonify(error='Username and password are required'), 400
    try:
        with sqlite3.connect(DB) as conn:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, hash_pwd(password)))
        return jsonify(msg='Registration successful'), 201
    except sqlite3.IntegrityError:
        return jsonify(error='Username already exists'), 400
    except Exception as e:
        return jsonify(error=f'Registration failed: {str(e)}'), 500

@app.post('/login')
def login():
    data = request.json
    username, password = data.get('username'), data.get('password')
    if not username or not password:
        return jsonify(error='Username and password are required'), 400
    with sqlite3.connect(DB) as conn:
        user = conn.execute(
            'SELECT id FROM users WHERE username=? AND password=?',
            (username, hash_pwd(password))
        ).fetchone()
    if user:
        return jsonify(user_id=user[0]), 200
    else:
        return jsonify(error='Invalid username or password'), 401

# ---------- 联系人 ----------
@app.post('/contacts')
def add_contact():
    data = request.json
    user_id, name, phone, email = data.get('user_id'), data.get('name'), data.get('phone'), data.get('email', '')
    if not all([user_id, name, phone]):
        return jsonify(error='User ID, name and phone are required'), 400
    try:
        with sqlite3.connect(DB) as conn:
            conn.execute(
                'INSERT INTO contacts (user_id, name, phone, email) VALUES (?, ?, ?, ?)',
                (user_id, name, phone, email))
        return jsonify(msg='Contact added successfully'), 201
    except Exception as e:
        return jsonify(error=f'Failed to add contact: {str(e)}'), 500

@app.get('/contacts/<int:user_id>')
def get_contacts(user_id):
    try:
        with sqlite3.connect(DB) as conn:
            rows = conn.execute(
                'SELECT id, name, phone, email FROM contacts WHERE user_id=?',
                (user_id,)
            ).fetchall()
        contacts = [{'id': r[0], 'name': r[1], 'phone': r[2], 'email': r[3]} for r in rows]
        return jsonify(contacts), 200
    except Exception as e:
        return jsonify(error=f'Failed to get contacts: {str(e)}'), 500

# ★ 新增：修改联系人
@app.put('/contacts/<int:contact_id>')
def update_contact(contact_id):
    data = request.json
    name, phone, email = data.get('name'), data.get('phone'), data.get('email', '')
    if not name or not phone:
        return jsonify(error='Name and phone are required'), 400
    try:
        with sqlite3.connect(DB) as conn:
            cur = conn.execute(
                'UPDATE contacts SET name=?, phone=?, email=? WHERE id=?',
                (name, phone, email, contact_id))
            if cur.rowcount == 0:
                return jsonify(error='Contact not found'), 404
        return jsonify(msg='Contact updated successfully'), 200
    except Exception as e:
        return jsonify(error=f'Failed to update contact: {str(e)}'), 500

@app.delete('/contacts/<int:contact_id>')
def delete_contact(contact_id):
    try:
        with sqlite3.connect(DB) as conn:
            conn.execute('DELETE FROM contacts WHERE id=?', (contact_id,))
        return jsonify(msg='Contact deleted successfully'), 200
    except Exception as e:
        return jsonify(error=f'Failed to delete contact: {str(e)}'), 500

@app.get('/contacts/count/<int:user_id>')
def count_contacts(user_id):
    try:
        with sqlite3.connect(DB) as conn:
            total = conn.execute('SELECT COUNT(*) FROM contacts WHERE user_id=?', (user_id,)).fetchone()[0]
        return jsonify(total=total), 200
    except Exception as e:
        return jsonify(error=f'Failed to count contacts: {str(e)}'), 500

# ---------- 启动 ----------
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5500)