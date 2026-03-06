import sqlite3
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet
import os
import json

DB_PATH = Path(__file__).parent / 'users.db'
ENCRYPTION_KEY_FILE = Path(__file__).parent / '.encryption_key'

def get_encryption_key():
    """Get or create encryption key for cookie storage"""
    if ENCRYPTION_KEY_FILE.exists():
        with open(ENCRYPTION_KEY_FILE, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_FILE, 'wb') as f:
            f.write(key)
        return key

ENCRYPTION_KEY = get_encryption_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

def init_db():
    """Initialize database with tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id TEXT,
            name_prefix TEXT,
            delay INTEGER DEFAULT 30,
            cookies_encrypted TEXT,
            messages TEXT,
            automation_running INTEGER DEFAULT 0,
            locked_group_name TEXT,
            locked_nicknames TEXT,
            lock_enabled INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Add missing columns to users table
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN admin_e2ee_thread_id TEXT')
        print("Added admin_e2ee_thread_id column to users table")
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute('ALTER TABLE users ADD COLUMN admin_chat_type TEXT')
        print("Added admin_chat_type column to users table")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Add missing columns to user_configs
    try:
        cursor.execute('ALTER TABLE user_configs ADD COLUMN automation_running INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute('ALTER TABLE user_configs ADD COLUMN locked_group_name TEXT')
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute('ALTER TABLE user_configs ADD COLUMN locked_nicknames TEXT')
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute('ALTER TABLE user_configs ADD COLUMN lock_enabled INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def encrypt_cookies(cookies):
    """Encrypt cookies for secure storage"""
    if not cookies:
        return None
    return cipher_suite.encrypt(cookies.encode()).decode()

def decrypt_cookies(encrypted_cookies):
    """Decrypt cookies"""
    if not encrypted_cookies:
        return ""
    try:
        return cipher_suite.decrypt(encrypted_cookies.encode()).decode()
    except:
        return ""

def create_user(username, password):
    """Create new user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        password_hash = hash_password(password)
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                      (username, password_hash))
        user_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO user_configs (user_id, chat_id, name_prefix, delay, messages)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, '', '', 30, ''))

        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists!"
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"

def verify_user(username, password):
    """Verify user credentials using SHA-256"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and user[1] == hash_password(password):
        return user[0]
    return None

def get_user_config(user_id):
    """Get user configuration"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT chat_id, name_prefix, delay, cookies_encrypted, messages, automation_running
        FROM user_configs WHERE user_id = ?
    ''', (user_id,))

    config = cursor.fetchone()
    conn.close()

    if config:
        return {
            'chat_id': config[0] or '',
            'name_prefix': config[1] or '',
            'delay': config[2] or 30,
            'cookies': decrypt_cookies(config[3]),
            'messages': config[4] or '',
            'automation_running': config[5] or 0
        }
    return None

def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages):
    """Update user configuration"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    encrypted_cookies = encrypt_cookies(cookies)

    cursor.execute('''
        UPDATE user_configs 
        SET chat_id = ?, name_prefix = ?, delay = ?, cookies_encrypted = ?, 
            messages = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (chat_id, name_prefix, delay, encrypted_cookies, messages, user_id))

    conn.commit()
    conn.close()

def get_username(user_id):
    """Get username by user ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    return user[0] if user else None

def set_automation_running(user_id, is_running):
    """Set automation running state for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE user_configs 
        SET automation_running = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (1 if is_running else 0, user_id))

    conn.commit()
    conn.close()

def get_automation_running(user_id):
    """Get automation running state for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT automation_running FROM user_configs WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()

    return bool(result[0]) if result else False

def get_lock_config(user_id):
    """Get lock configuration for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT chat_id, locked_group_name, locked_nicknames, lock_enabled, cookies_encrypted
        FROM user_configs WHERE user_id = ?
    ''', (user_id,))

    config = cursor.fetchone()
    conn.close()

    if config:
        try:
            nicknames = json.loads(config[2]) if config[2] else {}
        except:
            nicknames = {}

        return {
            'chat_id': config[0] or '',
            'locked_group_name': config[1] or '',
            'locked_nicknames': nicknames,
            'lock_enabled': bool(config[3]),
            'cookies': decrypt_cookies(config[4])
        }
    return None

def update_lock_config(user_id, chat_id, locked_group_name, locked_nicknames, cookies=None):
    """Update complete lock configuration including chat_id and cookies"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    nicknames_json = json.dumps(locked_nicknames)

    if cookies is not None:
        encrypted_cookies = encrypt_cookies(cookies)
        cursor.execute('''
            UPDATE user_configs 
            SET chat_id = ?, locked_group_name = ?, locked_nicknames = ?, 
                cookies_encrypted = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (chat_id, locked_group_name, nicknames_json, encrypted_cookies, user_id))
    else:
        cursor.execute('''
            UPDATE user_configs 
            SET chat_id = ?, locked_group_name = ?, locked_nicknames = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (chat_id, locked_group_name, nicknames_json, user_id))

    conn.commit()
    conn.close()

def set_lock_enabled(user_id, enabled):
    """Enable or disable the lock system"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE user_configs 
        SET lock_enabled = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (1 if enabled else 0, user_id))

    conn.commit()
    conn.close()

def get_lock_enabled(user_id):
    """Check if lock is enabled for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT lock_enabled FROM user_configs WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()

    return bool(result[0]) if result else False

# ==================== NEW FUNCTIONS FOR ADMIN NOTIFICATION ====================

def get_admin_e2ee_thread_id(user_id):
    """
    Get saved admin E2EE thread ID for a user
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT admin_e2ee_thread_id FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting admin thread ID: {e}")
        return None
    finally:
        conn.close()

def set_admin_e2ee_thread_id(user_id, thread_id, cookies, chat_type):
    """
    Save admin E2EE thread ID for a user
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE users 
            SET admin_e2ee_thread_id = ?, admin_chat_type = ? 
            WHERE id = ?
        """, (thread_id, chat_type, user_id))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error setting admin thread ID: {e}")
        return False
    finally:
        conn.close()

def get_all_users():
    """
    Get all users for admin panel
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT u.id, u.username, u.created_at, 
                   uc.chat_id, uc.automation_running,
                   u.admin_e2ee_thread_id, u.admin_chat_type
            FROM users u
            LEFT JOIN user_configs uc ON u.id = uc.user_id
            ORDER BY u.created_at DESC
        """)
        users = cursor.fetchall()
        return users
    except Exception as e:
        print(f"Error getting users: {e}")
        return []
    finally:
        conn.close()

def get_admin_chat_type(user_id):
    """
    Get saved admin chat type for a user
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT admin_chat_type FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting admin chat type: {e}")
        return None
    finally:
        conn.close()

# ==================== DATABASE MAINTENANCE ====================

def verify_database():
    """Verify database has all required columns"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check users table columns
    cursor.execute("PRAGMA table_info(users)")
    user_columns = [column[1] for column in cursor.fetchall()]
    print("Users table columns:", user_columns)
    
    # Check user_configs table columns
    cursor.execute("PRAGMA table_info(user_configs)")
    config_columns = [column[1] for column in cursor.fetchall()]
    print("User_configs table columns:", config_columns)
    
    conn.close()
    
    return {
        'users': user_columns,
        'user_configs': config_columns
    }

# Initialize database on import
init_db()

# Optional: Verify database on startup
if __name__ == "__main__":
    verify_database()