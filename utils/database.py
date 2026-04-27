import sqlite3
import os
from datetime import datetime, timedelta
import json

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'digital_buddy.db')

def get_db():
    """Получить соединение с базой данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Инициализировать базу данных"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Таблица новичков
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS newcomers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newcomer_id TEXT UNIQUE,
            name TEXT NOT NULL,
            position TEXT,
            department TEXT,
            start_date TEXT,
            mentor_name TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица сообщений чата
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newcomer_id TEXT,
            message TEXT NOT NULL,
            sender TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (newcomer_id) REFERENCES newcomers(newcomer_id)
        )
    ''')
    
    # Таблица настроений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newcomer_id TEXT,
            mood_score INTEGER,
            feedback TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (newcomer_id) REFERENCES newcomers(newcomer_id)
        )
    ''')
    
    # Таблица алертов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newcomer_id TEXT,
            level TEXT,
            reason TEXT,
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (newcomer_id) REFERENCES newcomers(newcomer_id)
        )
    ''')
    
    # Таблица сессий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newcomer_id TEXT UNIQUE,
            token TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (newcomer_id) REFERENCES newcomers(newcomer_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_newcomer(name, position, department, start_date, mentor_name=""):
    """Добавить нового новичка"""
    conn = get_db()
    cursor = conn.cursor()
    
    newcomer_id = f"NB-{datetime.now().strftime('%Y%m%d')}-{hash(name) % 10000:04d}"
    
    try:
        cursor.execute('''
            INSERT INTO newcomers (newcomer_id, name, position, department, start_date, mentor_name)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (newcomer_id, name, position, department, start_date, mentor_name))
        conn.commit()
        return newcomer_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_newcomer(newcomer_id):
    """Получить информацию о новичке"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM newcomers WHERE newcomer_id = ?', (newcomer_id,))
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None

def get_all_newcomers():
    """Получить всех новичков"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM newcomers ORDER BY start_date DESC')
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def add_message(newcomer_id, message, sender):
    """Добавить сообщение в чат"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (newcomer_id, message, sender)
        VALUES (?, ?, ?)
    ''', (newcomer_id, message, sender))
    conn.commit()
    conn.close()

def get_messages(newcomer_id, limit=50):
    """Получить историю сообщений"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM messages 
        WHERE newcomer_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (newcomer_id, limit))
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def add_mood_checkin(newcomer_id, mood_score, feedback=""):
    """Добавить проверку настроения"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mood_checkins (newcomer_id, mood_score, feedback)
        VALUES (?, ?, ?)
    ''', (newcomer_id, mood_score, feedback))
    conn.commit()
    conn.close()

def get_mood_history(newcomer_id, days=30):
    """Получить историю настроения"""
    conn = get_db()
    cursor = conn.cursor()
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT * FROM mood_checkins 
        WHERE newcomer_id = ? AND created_at >= ?
        ORDER BY created_at ASC
    ''', (newcomer_id, cutoff_date))
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def add_alert(newcomer_id, level, reason):
    """Добавить алерт"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alerts (newcomer_id, level, reason)
        VALUES (?, ?, ?)
    ''', (newcomer_id, level, reason))
    conn.commit()
    conn.close()

def get_active_alerts():
    """Получить активные алерты"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, n.name as newcomer_name 
        FROM alerts a 
        JOIN newcomers n ON a.newcomer_id = n.newcomer_id 
        WHERE a.status = 'active'
        ORDER BY a.created_at DESC
    ''')
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def resolve_alert(alert_id):
    """Разрешить алерт"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE alerts SET status = 'resolved' WHERE id = ?
    ''', (alert_id,))
    conn.commit()
    conn.close()

def create_session(newcomer_id):
    """Создать сессию для новичка"""
    conn = get_db()
    cursor = conn.cursor()
    token = f"tok_{newcomer_id}_{datetime.now().timestamp()}"
    cursor.execute('''
        INSERT OR REPLACE INTO sessions (newcomer_id, token)
        VALUES (?, ?)
    ''', (newcomer_id, token))
    conn.commit()
    conn.close()
    return token

def verify_session(token):
    """Проверить сессию"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT newcomer_id FROM sessions WHERE token = ?
    ''', (token,))
    result = cursor.fetchone()
    conn.close()
    return result['newcomer_id'] if result else None

def get_dashboard_summary():
    """Получить сводку для дашборда"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Общее количество новичков
    cursor.execute('SELECT COUNT(*) as count FROM newcomers')
    total = cursor.fetchone()['count']
    
    # Активные алерты
    cursor.execute("SELECT COUNT(*) as count FROM alerts WHERE status = 'active'")
    alerts = cursor.fetchone()['count']
    
    # Среднее настроение за неделю
    cutoff_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute(f'''
        SELECT AVG(mood_score) as avg_mood FROM mood_checkins 
        WHERE created_at >= ?
    ''', (cutoff_date,))
    avg_mood = cursor.fetchone()['avg_mood'] or 0
    
    conn.close()
    
    return {
        'total_newcomers': total,
        'active_alerts': alerts,
        'avg_mood': round(avg_mood, 2)
    }

# Инициализировать БД при импорте
init_db()
