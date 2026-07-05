from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to call API

# Database initialization
DB_PATH = os.path.join(os.path.dirname(__file__), 'todos.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB when app starts
init_db()

# API Routes
@app.route('/api/todos', methods=['GET'])
def get_todos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    todos = cursor.execute('SELECT id, title, completed FROM todos').fetchall()
    conn.close()
    return jsonify([{'id': t[0], 'title': t[1], 'completed': bool(t[2])} for t in todos])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.json
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todos (title) VALUES (?)', (title,))
    conn.commit()
    todo_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': todo_id, 'title': title, 'completed': False}), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    completed = data.get('completed')
    title = data.get('title')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if title:
        cursor.execute('UPDATE todos SET title = ? WHERE id = ?', (title, todo_id))
    if completed is not None:
        cursor.execute('UPDATE todos SET completed = ? WHERE id = ?', (completed, todo_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Todo updated'}), 200

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo deleted'}), 200

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)