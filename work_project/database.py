import sqlite3


def create_database():
    conn = sqlite3.connect('photo_information.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x INTEGER,
            y INTEGER,
            image_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def insert_event(x, y, image_path):
    conn = sqlite3.connect('photo_information.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (x, y, image_path) VALUES (?, ?, ?)
    ''', (x, y, image_path))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()