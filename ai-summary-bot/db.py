import sqlite3
from datetime import datetime

conn = sqlite3.connect("messages.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    username TEXT,
    text TEXT,
    timestamp TEXT
)
''')
conn.commit()

def save_message(chat_id, username, text, timestamp):
    cursor.execute('''
        INSERT INTO messages (chat_id, username, text, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (chat_id, username, text, timestamp))
    conn.commit()

def get_weekly_messages():
    cursor.execute('''
        SELECT username, text, timestamp FROM messages
        WHERE timestamp >= datetime('now', '-7 days')
        ORDER BY timestamp ASC
    ''')
    return cursor.fetchall()
