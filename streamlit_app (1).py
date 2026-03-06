import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import subprocess
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests
import gc
import tempfile
from datetime import datetime

st.set_page_config(
    page_title="E2E YAMRAJ",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 👑 GOLD & BLACK THEME with your photo
custom_css = """
<style>
    /* Clean font for everyone */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Background with your photo */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.9)),
                          url('https://i.ibb.co/Rkp3VcHy/image.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .main .block-container {
        background: rgba(0, 0, 0, 0.75);
        border-radius: 20px;
        padding: 30px;
        border: 2px solid #FFD700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
    }

    /* Admin Panel Header */
    .admin-header {
        background: linear-gradient(135deg, #000000, #1a1a1a);
        border: 2px solid #FFD700;
        color: #FFD700;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
    }
    
    .admin-header h1 {
        margin: 0;
        font-size: 2.2rem;
        color: #FFD700;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }

    /* User Panel Header */
    .user-header {
        background: linear-gradient(135deg, #000000, #1a1a1a);
        border: 2px solid #FFD700;
        color: #FFD700;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
    }
    
    .user-header h1 {
        margin: 0;
        font-size: 2.2rem;
        color: #FFD700;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }

    /* Login Header with your photo */
    .login-header {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid #FFD700;
        border-radius: 15px;
    }
    
    .login-header h1 {
        color: #FFD700;
        font-size: 2.5rem;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
        margin: 10px 0;
    }
    
    .login-header p {
        color: #FFD700;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .profile-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 3px solid #FFD700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        margin-bottom: 15px;
    }

    /* Category Badges */
    .admin-badge {
        background: #000000;
        border: 2px solid #FFD700;
        color: #FFD700;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 5px;
        font-weight: bold;
    }
    
    .user-badge {
        background: #000000;
        border: 2px solid #FFD700;
        color: #FFD700;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 5px;
        font-weight: bold;
    }
    
    .pending-badge {
        background: #000000;
        border: 2px solid #FFA500;
        color: #FFA500;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 5px;
        font-weight: bold;
    }

    /* Buttons */
    .stButton>button {
        background: #000000;
        color: #FFD700;
        border: 2px solid #FFD700;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: #FFD700;
        color: #000000;
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.5);
    }

    /* START Button - Gold */
    div[data-testid="column"]:nth-of-type(1) .stButton>button {
        background: #000000;
        color: #00FF00;
        border: 2px solid #00FF00;
    }
    div[data-testid="column"]:nth-of-type(1) .stButton>button:hover {
        background: #00FF00;
        color: #000000;
    }
    
    /* STOP Button - Red */
    div[data-testid="column"]:nth-of-type(2) .stButton>button {
        background: #000000;
        color: #FF4444;
        border: 2px solid #FF4444;
    }
    div[data-testid="column"]:nth-of-type(2) .stButton>button:hover {
        background: #FF4444;
        color: #000000;
    }
    
    /* CLOSE ALL Button - Gold with pulse */
    div[data-testid="column"]:nth-of-type(3) .stButton>button {
        background: #000000;
        color: #FFD700;
        border: 2px solid #FFD700;
        animation: goldPulse 2s infinite;
    }
    div[data-testid="column"]:nth-of-type(3) .stButton>button:hover {
        background: #FFD700;
        color: #000000;
    }
    
    @keyframes goldPulse {
        0% { box-shadow: 0 0 5px #FFD700; }
        50% { box-shadow: 0 0 20px #FFD700; }
        100% { box-shadow: 0 0 5px #FFD700; }
    }

    /* Input Fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid #FFD700;
        border-radius: 10px;
        padding: 12px;
        font-size: 1rem;
        color: #FFD700;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #FFD700;
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.3);
        background: #000000;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #FFD70080;
    }

    /* Labels */
    label {
        color: #FFD700 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #FFD700;
        font-size: 2rem;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    [data-testid="stMetricLabel"] {
        color: #FFD700;
        font-weight: 500;
        opacity: 0.9;
    }

    /* Console Output */
    .console-output {
        background: #000000;
        border: 2px solid #FFD700;
        border-radius: 10px;
        padding: 15px;
        color: #00FF00;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        max-height: 400px;
        overflow-y: auto;
    }

    .console-line {
        border-bottom: 1px solid #FFD70020;
        padding: 5px 10px;
        margin: 3px 0;
        font-family: 'Courier New', monospace;
    }
    
    .console-line-success { color: #00FF00; }
    .console-line-error { color: #FF4444; }
    .console-line-info { color: #FFD700; }
    .console-line-send { color: #00FFFF; }

    /* Status Box */
    .status-box {
        background: #000000;
        border: 2px solid #FFD700;
        color: #FFD700;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
    }
    
    .status-box h3 {
        margin: 0;
        font-size: 1.5rem;
        color: #FFD700;
    }

    /* Secret Key Display */
    .secret-key {
        background: #000000;
        padding: 15px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        text-align: center;
        border: 2px dashed #FFD700;
        margin: 10px 0;
        color: #FFD700;
    }

    /* Login Boxes */
    .login-box {
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid #FFD700;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
    }
    
    .login-box h2 {
        color: #FFD700;
        margin-bottom: 10px;
    }
    
    .login-box p {
        color: #FFD700;
        opacity: 0.8;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #FFD700;
        padding: 20px;
        font-size: 0.9rem;
        border-top: 1px solid #FFD700;
        margin-top: 30px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #000000;
        border: 2px solid #FFD700;
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #FFD700;
        border-radius: 8px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: #FFD700;
        color: #000000;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #000000 !important;
        color: #FFD700 !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        background: #000000 !important;
        color: #FFD700 !important;
        border: 2px solid #FFD700 !important;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1wrcr25 {
        background: #000000 !important;
        border-right: 2px solid #FFD700 !important;
    }
    
    .sidebar-content {
        color: #FFD700 !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ==================== CONSTANTS ====================
WHATSAPP_NUMBER = "7654221354"  # Admin ka WhatsApp number
ADMIN_SECRET_PASSWORD = "YAMRAJ2025"  # Admin direct login password
APPROVAL_FILE = "approved_users.json"
PENDING_FILE = "pending_users.json"
USERS_FILE = "registered_users.json"

# ==================== HELPER FUNCTIONS ====================
def generate_secret_key(username, password):
    """Generate unique secret key for user"""
    combined = f"{username}:{password}:{time.time()}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:12].upper()
    return f"KEY-{key_hash}"

def load_json_file(filename, default={}):
    """Load JSON file safely"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return default
    return default

def save_json_file(filename, data):
    """Save JSON file safely"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def load_approved_users():
    return load_json_file(APPROVAL_FILE, {})

def save_approved_users(users):
    save_json_file(APPROVAL_FILE, users)

def load_pending_users():
    return load_json_file(PENDING_FILE, {})

def save_pending_users(users):
    save_json_file(PENDING_FILE, users)

def load_registered_users():
    return load_json_file(USERS_FILE, {})

def save_registered_users(users):
    save_json_file(USERS_FILE, users)

def send_whatsapp_notification(username, secret_key):
    """Send secret key to admin WhatsApp"""
    message = f"""👑 NEW USER REGISTRATION - YAMRAJ SYSTEM 👑

👤 Username: {username}
🔑 Secret Key: {secret_key}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please approve this user in Admin Panel!"""
    
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_user_approval(username):
    """Check if user is approved"""
    approved = load_approved_users()
    return username in approved

def register_new_user(username, password):
    """Register new user and add to pending"""
    # Check if user already exists
    registered = load_registered_users()
    if username in registered:
        return False, "Username already exists!"
    
    # Generate secret key
    secret_key = generate_secret_key(username, password)
    
    # Save registered user
    registered[username] = {
        "username": username,
        "password": password,  # In production, hash this!
        "secret_key": secret_key,
        "registered_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "status": "pending"
    }
    save_registered_users(registered)
    
    # Add to pending approvals
    pending = load_pending_users()
    pending[username] = {
        "username": username,
        "secret_key": secret_key,
        "requested_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_pending_users(pending)
    
    return True, secret_key

# ==================== SESSION STATE ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:  # 'admin' or 'user'
    st.session_state.user_type = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'secret_key' not in st.session_state:
    st.session_state.secret_key = None
if 'user_approved' not in st.session_state:
    st.session_state.user_approved = False
if 'pending_status' not in st.session_state:
    st.session_state.pending_status = None
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'show_close_confirmation' not in st.session_state:
    st.session_state.show_close_confirmation = False
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()
if 'messages_content' not in st.session_state:
    st.session_state.messages_content = ""

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0
        self.driver = None
        self.current_chat_id = None
        self.speed = 0
        self.total_messages = 0
        self.start_time = None

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

# ==================== LOGGING FUNCTION ====================
def log_message(msg, msg_type="info", automation_state=None):
    now = datetime.now()
    timestamp = now.strftime("%I:%M:%S %p")
    
    emoji_map = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "send": "📤",
        "load": "📥",
        "info": "ℹ️"
    }
    emoji = emoji_map.get(msg_type, "ℹ️")
    
    formatted_msg = f"[{timestamp}] {emoji} {msg}"
   
    if automation_state:
        automation_state.logs.append(formatted_msg)
        if len(automation_state.logs) > 100:
            automation_state.logs = automation_state.logs[-100:]
    else:
        st.session_state.logs.append(formatted_msg)
        if len(st.session_state.logs) > 100:
            st.session_state.logs = st.session_state.logs[-100:]
    
    return formatted_msg

# ==================== AUTOMATION FUNCTIONS ====================
def setup_browser(automation_state=None):
    """Setup Chrome browser with proper options"""
    log_message('Setting up Chrome browser...', "info", automation_state)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    # Try to find Chrome/Chromium
    chrome_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for path in chrome_paths:
        if Path(path).exists():
            chrome_options.binary_location = path
            log_message(f'Found browser at: {path}', "info", automation_state)
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Try using webdriver-manager first
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Browser started with webdriver-manager!', "success", automation_state)
        except:
            # Fallback to default
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Browser started with default driver!', "success", automation_state)
        
        driver.set_window_size(1920, 1080)
        log_message('Browser setup completed!', "success", automation_state)
        return driver
        
    except Exception as error:
        log_message(f'Browser setup failed: {error}', "error", automation_state)
        raise error

def find_message_input(driver, process_id, automation_state=None):
    """Find message input field in Facebook"""
    log_message(f'{process_id}: Finding message input...', "info", automation_state)
    time.sleep(5)
    
    # Scroll to load all elements
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except:
        pass
    
    # Message input selectors
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed():
                    log_message(f'✅ Found message input', "success", automation_state)
                    return element
        except:
            continue
    
    log_message(f'❌ Message input not found!', "error", automation_state)
    return None

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    """Main function to send messages"""
    driver = None
    try:
        # Record start time
        automation_state.start_time = datetime.now()
        
        # Load messages
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        total_msgs = len(messages_list)
        automation_state.total_messages = total_msgs
        
        # Calculate total characters
        total_chars = sum(len(msg) for msg in messages_list)
        log_message(f'Message loaded: {total_chars} chars', "load", automation_state)
        log_message(f'Starting FAST send to 1 threads', "info", automation_state)
        
        delay = int(config['delay'])
        delay_ms = delay * 1000
        log_message(f'Speed: {delay_ms}ms delay', "info", automation_state)
        
        # Setup browser
        driver = setup_browser(automation_state)
        automation_state.driver = driver
        
        # Navigate to Facebook
        log_message(f'Navigating to Facebook...', "info", automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(5)
        
        # Add cookies if available
        if config['cookies'] and config['cookies'].strip():
            log_message(f'Adding cookies...', "info", automation_state)
            try:
                cookie_pairs = config['cookies'].split(';')
                for cookie in cookie_pairs:
                    if '=' in cookie:
                        name, value = cookie.split('=', 1)
                        driver.add_cookie({
                            'name': name.strip(),
                            'value': value.strip(),
                            'domain': '.facebook.com'
                        })
            except Exception as e:
                log_message(f'Cookie error: {str(e)[:50]}', "warning", automation_state)
        
        # Open conversation
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            automation_state.current_chat_id = chat_id
            log_message(f'Opening conversation {chat_id}...', "info", automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
            time.sleep(8)
        else:
            log_message(f'Opening messages...', "info", automation_state)
            driver.get('https://www.facebook.com/messages')
            time.sleep(8)
        
        # Find message input
        message_input = find_message_input(driver, process_id, automation_state)
        if not message_input:
            log_message(f'❌ Could not find message input!', "error", automation_state)
            return 0
        
        # Send messages
        messages_sent = 0
        for i, message in enumerate(messages_list):
            if not automation_state.running:
                break
            
            try:
                # Add prefix if exists
                if config['name_prefix']:
                    full_message = f"{config['name_prefix']} {message}"
                else:
                    full_message = message
                
                # Type message
                driver.execute_script("arguments[0].focus();", message_input)
                message_input.clear()
                message_input.send_keys(full_message)
                time.sleep(1)
                
                # Send message
                message_input.send_keys(Keys.RETURN)
                
                messages_sent += 1
                automation_state.message_count = messages_sent
                
                log_message(f"[{chat_id}] Message {messages_sent}/{total_msgs} sent", "send", automation_state)
                
                # Wait for delay
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'Send error: {str(e)[:100]}', "error", automation_state)
                time.sleep(5)
        
        log_message(f'✅ All messages sent successfully!', "success", automation_state)
        log_message(f'Total: {messages_sent} messages sent', "success", automation_state)
        
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return messages_sent
        
    except Exception as e:
        log_message(f'Fatal error: {str(e)}', "error", automation_state)
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f'Browser closed', "info", automation_state)
            except:
                pass

def start_automation(user_config, user_id):
    """Start automation in background thread"""
    if st.session_state.automation_state.running:
        return
    
    st.session_state.automation_state.running = True
    st.session_state.automation_state.message_count = 0
    st.session_state.automation_state.logs = []
    st.session_state.automation_state.current_chat_id = user_config['chat_id']
    st.session_state.automation_state.start_time = datetime.now()
    
    db.set_automation_running(user_id, True)
    
    thread = threading.Thread(
        target=send_messages,
        args=(user_config, st.session_state.automation_state, user_id)
    )
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    """Stop automation"""
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)
    log_message("Automation stopped by user", "warning", st.session_state.automation_state)

def close_all_tasks():
    """Close all tasks and clean up"""
    with st.spinner("🧹 Cleaning up all tasks..."):
        # Stop automation
        if st.session_state.automation_state.running:
            st.session_state.automation_state.running = False
        
        # Close browser
        if hasattr(st.session_state.automation_state, 'driver') and st.session_state.automation_state.driver:
            try:
                st.session_state.automation_state.driver.quit()
            except:
                pass
        
        # Kill processes
        try:
            os.system("pkill -f chrome")
            os.system("pkill -f chromedriver")
        except:
            pass
        
        # Reset session
        st.session_state.automation_state.message_count = 0
        st.session_state.automation_state.logs = []
        st.session_state.automation_state.message_rotation_index = 0
        
        # Clean temp files
        try:
            temp_dir = tempfile.gettempdir()
            for file in os.listdir(temp_dir):
                if file.startswith('tmp') and file.endswith('.log'):
                    os.remove(os.path.join(temp_dir, file))
        except:
            pass
        
        gc.collect()
        time.sleep(2)
        st.success("✅ All tasks closed successfully!")

# ==================== PAGE FUNCTIONS ====================
def admin_page():
    """Admin Panel - User Approval Management + Message Dashboard"""
    
    # Admin tabs - Approval Panel + Message Dashboard
    tab1, tab2 = st.tabs(["👑 APPROVAL PANEL", "🤖 MESSAGE DASHBOARD"])
    
    with tab1:
        st.markdown("""
        <div class="admin-header">
            <h1>👑 ADMIN APPROVAL PANEL</h1>
            <p>Manage User Approvals</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Load data
        pending = load_pending_users()
        approved = load_approved_users()
        registered = load_registered_users()
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Registered", len(registered))
        with col2:
            st.metric("Pending Approval", len(pending))
        with col3:
            st.metric("Approved Users", len(approved))
        
        st.markdown("---")
        
        # Pending Approvals Section
        if pending:
            st.markdown("### ⏳ PENDING APPROVALS")
            
            for username, data in pending.items():
                with st.expander(f"👤 {username} - Requested: {data['requested_at']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Username:** {username}")
                        st.markdown(f"**Secret Key:** `{data['secret_key']}`")
                        st.markdown(f"**Request Time:** {data['requested_at']}")
                    
                    with col2:
                        if st.button("✅ APPROVE", key=f"approve_{username}"):
                            # Add to approved
                            approved[username] = {
                                "username": username,
                                "secret_key": data['secret_key'],
                                "approved_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            save_approved_users(approved)
                            
                            # Update registered user status
                            if username in registered:
                                registered[username]['status'] = 'approved'
                                registered[username]['approved_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                save_registered_users(registered)
                            
                            # Remove from pending
                            del pending[username]
                            save_pending_users(pending)
                            
                            st.success(f"✅ User {username} approved!")
                            st.rerun()
                        
                        if st.button("❌ REJECT", key=f"reject_{username}"):
                            # Update registered user status
                            if username in registered:
                                registered[username]['status'] = 'rejected'
                                save_registered_users(registered)
                            
                            # Remove from pending
                            del pending[username]
                            save_pending_users(pending)
                            
                            st.error(f"❌ User {username} rejected!")
                            st.rerun()
        else:
            st.info("No pending approvals")
        
        st.markdown("---")
        
        # Approved Users Section
        if approved:
            st.markdown("### ✅ APPROVED USERS")
            for username in approved.keys():
                st.markdown(f"👤 **{username}**")
    
    with tab2:
        st.markdown("""
        <div class="admin-header">
            <h1>🤖 ADMIN MESSAGE DASHBOARD</h1>
            <p>Send Messages as Admin</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Admin ka alag config
        admin_username = "admin"
        admin_password = ADMIN_SECRET_PASSWORD
        
        # Get or create admin user
        admin_id = db.verify_user(admin_username, admin_password)
        if not admin_id:
            success, msg = db.create_user(admin_username, admin_password)
            if success:
                admin_id = db.verify_user(admin_username, admin_password)
        
        if admin_id:
            admin_config = db.get_user_config(admin_id)
            
            if admin_config:
                st.markdown("### Admin Configuration")
                
                chat_id = st.text_input("Chat/Conversation ID", value=admin_config['chat_id'],
                                       placeholder="e.g., 1362400298935018", key="admin_chat")
                
                name_prefix = st.text_input("Hatersname", value=admin_config['name_prefix'],
                                           placeholder="e.g., [ADMIN]", key="admin_prefix")
                
                delay = st.number_input("Delay (seconds)", min_value=1, max_value=300,
                                       value=admin_config['delay'], key="admin_delay")
                
                cookies = st.text_area("Facebook Cookies", value=admin_config['cookies'],
                                      placeholder="Paste your cookies here...", height=150, key="admin_cookies",
                                      help="Format: cookie1=value1; cookie2=value2")
                
                # File upload for messages
                uploaded_file = st.file_uploader("Upload Messages File (np.txt)", type=['txt'], key="admin_upload")
                if uploaded_file:
                    messages = uploaded_file.read().decode('utf-8')
                    st.session_state.admin_messages = messages
                    st.success(f"✅ Uploaded {len(messages.splitlines())} messages")
                else:
                    messages = st.session_state.get('admin_messages', admin_config['messages'])
                
                messages = st.text_area("Messages (one per line)", value=messages,
                                       placeholder="Enter messages...", height=200, key="admin_messages")
                
                if st.button("💾 Save Admin Config", use_container_width=True):
                    if db.update_user_config(admin_id, chat_id, name_prefix, delay, cookies, messages):
                        st.success("✅ Admin config saved!")
                        st.rerun()
                
                st.markdown("---")
                
                # Status metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Messages Sent", st.session_state.automation_state.message_count)
                with col2:
                    status = "🟢 Running" if st.session_state.automation_state.running else "🔴 Stopped"
                    st.metric("Status", status)
                with col3:
                    chat_display = chat_id[:10] + "..." if chat_id and len(chat_id) > 10 else chat_id or "Not Set"
                    st.metric("Chat ID", chat_display)
                
                st.markdown("---")
                
                # Control buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    start_disabled = st.session_state.automation_state.running or not chat_id or not cookies
                    if st.button("▶️ START ADMIN", disabled=start_disabled, use_container_width=True):
                        if chat_id and cookies:
                            # Update config before starting
                            admin_config = {
                                'chat_id': chat_id,
                                'name_prefix': name_prefix,
                                'delay': delay,
                                'cookies': cookies,
                                'messages': messages
                            }
                            start_automation(admin_config, admin_id)
                            st.success("✅ Admin automation started!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Set Chat ID and Cookies first!")
                
                with col2:
                    if st.button("⏹️ STOP ADMIN", disabled=not st.session_state.automation_state.running, use_container_width=True):
                        stop_automation(admin_id)
                        st.warning("⏹️ Admin automation stopped!")
                        time.sleep(1)
                        st.rerun()
                
                with col3:
                    if st.button("🗑️ CLOSE ALL", use_container_width=True):
                        st.session_state.show_close_confirmation = True
                
                # Confirmation dialog for CLOSE ALL
                if st.session_state.show_close_confirmation:
                    st.markdown("""
                    <div style="background: #000000; border: 2px solid #FFD700; padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
                        <h3 style="color: #FFD700;">⚠️ WARNING</h3>
                        <p style="color: #FFD700;">Are you sure you want to close ALL tasks?</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ YES", use_container_width=True):
                            st.session_state.show_close_confirmation = False
                            close_all_tasks()
                            st.rerun()
                    with col2:
                        if st.button("❌ NO", use_container_width=True):
                            st.session_state.show_close_confirmation = False
                            st.rerun()
                
                # Auto-refresh when running
                if st.session_state.automation_state.running:
                    time.sleep(2)
                    st.rerun()
                
                # Live logs
                if st.session_state.automation_state.logs:
                    st.markdown("### 📟 Live Logs")
                    logs_html = '<div class="console-output">'
                    for log in st.session_state.automation_state.logs[-30:]:
                        log_class = "console-line-info"
                        if "✅" in log:
                            log_class = "console-line-success"
                        elif "❌" in log:
                            log_class = "console-line-error"
                        elif "📤" in log:
                            log_class = "console-line-send"
                        logs_html += f'<div class="console-line {log_class}">{log}</div>'
                    logs_html += '</div>'
                    
                    st.markdown(logs_html, unsafe_allow_html=True)
                    
                    # Auto-scroll JavaScript
                    st.markdown("""
                    <script>
                        setTimeout(function() {
                            var consoleDiv = document.querySelector('.console-output');
                            if (consoleDiv) consoleDiv.scrollTop = consoleDiv.scrollHeight;
                        }, 100);
                    </script>
                    """, unsafe_allow_html=True)

def user_pending_page(username, secret_key):
    """Page shown to user while waiting for approval"""
    st.markdown("""
    <div class="user-header">
        <h1>⏳ APPROVAL PENDING</h1>
        <p>Your account is waiting for admin approval</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Your Details")
        st.markdown(f"**Username:** {username}")
        st.markdown(f"**Secret Key:** `{secret_key}`")
        st.markdown(f"**Status:** ⏳ Pending Approval")
    
    with col2:
        st.markdown("### 📱 Contact Admin")
        whatsapp_url = send_whatsapp_notification(username, secret_key)
        
        st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
            <div style="background: #000000; border: 2px solid #FFD700; color: #FFD700; padding: 15px; border-radius: 10px; text-align: center;">
                📱 Contact Admin on WhatsApp
            </div>
        </a>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #000000; border: 2px solid #FFD700; padding: 15px; border-radius: 10px; margin-top: 10px;">
            <p style="margin:0; color: #FFD700;">Admin will approve your account soon. Check back after approval.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Check approval status button
    if st.button("🔄 Check Approval Status", use_container_width=True):
        if check_user_approval(username):
            st.session_state.user_approved = True
            st.session_state.pending_status = None
            st.success("✅ Your account is approved! Redirecting...")
            time.sleep(2)
            st.rerun()
        else:
            st.warning("⏳ Still pending approval")
    
    # Logout
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

def user_page():
    """Main User Dashboard"""
    st.markdown("""
    <div class="user-header">
        <h1>👤 USER DASHBOARD</h1>
        <p>Facebook Message Automation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar user info
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.markdown(f"**Secret Key:** `{st.session_state.secret_key}`")
        st.markdown("**Status:** ✅ Approved")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.rerun()
    
    # Main content
    user_config = db.get_user_config(st.session_state.user_id) if st.session_state.user_id else None
    
    if not user_config:
        # Try to get from registered users
        registered = load_registered_users()
        if st.session_state.username in registered:
            success, user_id = db.create_user(
                st.session_state.username,
                registered[st.session_state.username]['password']
            )
            if success:
                st.session_state.user_id = user_id
                user_config = db.get_user_config(user_id)
    
    if user_config:
        tab1, tab2 = st.tabs(["⚙️ Configuration", "🤖 Automation"])
        
        with tab1:
            st.markdown("### Your Configuration")
            
            chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'],
                                   placeholder="e.g., 1362400298935018")
            
            name_prefix = st.text_input("Hatersname", value=user_config['name_prefix'],
                                       placeholder="e.g., [END TO END]")
            
            delay = st.number_input("Delay (seconds)", min_value=1, max_value=300,
                                   value=user_config['delay'])
            
            cookies = st.text_area("Facebook Cookies", value=user_config['cookies'],
                                  placeholder="Paste your cookies here...", height=150,
                                  help="Format: cookie1=value1; cookie2=value2")
            
            # File upload for messages
            uploaded_file = st.file_uploader("Upload Messages File (np.txt)", type=['txt'])
            if uploaded_file:
                messages = uploaded_file.read().decode('utf-8')
                st.session_state.messages_content = messages
                st.success(f"✅ Uploaded {len(messages.splitlines())} messages")
            else:
                messages = st.session_state.get('messages_content', user_config['messages'])
            
            messages = st.text_area("Messages (one per line)", value=messages,
                                   placeholder="Enter messages...", height=200)
            
            if st.button("💾 Save Configuration", use_container_width=True):
                if db.update_user_config(st.session_state.user_id, chat_id, name_prefix, delay, cookies, messages):
                    st.success("✅ Configuration saved!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save configuration")
        
        with tab2:
            st.markdown("### Automation Control")
            
            # Status metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Messages Sent", st.session_state.automation_state.message_count)
            with col2:
                status = "🟢 Running" if st.session_state.automation_state.running else "🔴 Stopped"
                st.metric("Status", status)
            with col3:
                chat_display = user_config['chat_id'][:10] + "..." if user_config['chat_id'] and len(user_config['chat_id']) > 10 else user_config['chat_id'] or "Not Set"
                st.metric("Chat ID", chat_display)
            
            st.markdown("---")
            
            # Control buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                start_disabled = st.session_state.automation_state.running or not user_config['chat_id'] or not user_config['cookies']
                if st.button("▶️ START", disabled=start_disabled, use_container_width=True):
                    if user_config['chat_id'] and user_config['cookies']:
                        start_automation(user_config, st.session_state.user_id)
                        st.success("✅ Automation started!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Set Chat ID and Cookies first!")
            
            with col2:
                if st.button("⏹️ STOP", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.warning("⏹️ Automation stopped!")
                    time.sleep(1)
                    st.rerun()
            
            with col3:
                if st.button("🗑️ CLOSE ALL", use_container_width=True):
                    st.session_state.show_close_confirmation = True
            
            # Confirmation dialog for CLOSE ALL
            if st.session_state.show_close_confirmation:
                st.markdown("""
                <div style="background: #000000; border: 2px solid #FFD700; padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
                    <h3 style="color: #FFD700;">⚠️ WARNING</h3>
                    <p style="color: #FFD700;">Are you sure you want to close ALL tasks?</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ YES", use_container_width=True):
                        st.session_state.show_close_confirmation = False
                        close_all_tasks()
                        st.rerun()
                with col2:
                    if st.button("❌ NO", use_container_width=True):
                        st.session_state.show_close_confirmation = False
                        st.rerun()
            
            # Auto-refresh when running
            if st.session_state.automation_state.running:
                time.sleep(2)
                st.rerun()
            
            # Live logs
            if st.session_state.automation_state.logs:
                st.markdown("### 📟 Live Logs")
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-30:]:
                    log_class = "console-line-info"
                    if "✅" in log:
                        log_class = "console-line-success"
                    elif "❌" in log:
                        log_class = "console-line-error"
                    elif "📤" in log:
                        log_class = "console-line-send"
                    logs_html += f'<div class="console-line {log_class}">{log}</div>'
                logs_html += '</div>'
                
                st.markdown(logs_html, unsafe_allow_html=True)
                
                # Auto-scroll JavaScript
                st.markdown("""
                <script>
                    setTimeout(function() {
                        var consoleDiv = document.querySelector('.console-output');
                        if (consoleDiv) consoleDiv.scrollTop = consoleDiv.scrollHeight;
                    }, 100);
                </script>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No configuration found. Please contact admin.")

def login_page():
    """Main Login/Registration Page"""
    st.markdown(f"""
    <div class="login-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="profile-img">
        <h1>👑 E2E YAMRAJ SYSTEM</h1>
        <p>Facebook Message Automation Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="login-box">
            <h2>👤 USER LOGIN</h2>
            <p>For approved users only</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("user_login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("🔑 Login as User", use_container_width=True)
            
            if submitted:
                if username and password:
                    # Check registered users
                    registered = load_registered_users()
                    if username in registered and registered[username]['password'] == password:
                        # Check if approved
                        if check_user_approval(username):
                            # Get or create user_id from database
                            user_id = db.verify_user(username, password)
                            if not user_id:
                                success, msg = db.create_user(username, password)
                                if success:
                                    user_id = db.verify_user(username, password)
                            
                            if user_id:
                                st.session_state.logged_in = True
                                st.session_state.user_type = 'user'
                                st.session_state.username = username
                                st.session_state.user_id = user_id
                                st.session_state.secret_key = registered[username]['secret_key']
                                st.session_state.user_approved = True
                                st.success("✅ Login successful!")
                                st.rerun()
                            else:
                                st.error("❌ Database error!")
                        else:
                            # Show pending page
                            st.session_state.logged_in = True
                            st.session_state.user_type = 'pending'
                            st.session_state.username = username
                            st.session_state.secret_key = registered[username]['secret_key']
                            st.session_state.pending_status = 'pending'
                            st.rerun()
                    else:
                        st.error("❌ Invalid username or password!")
                else:
                    st.warning("⚠️ Fill all fields!")
    
    with col2:
        st.markdown("""
        <div class="login-box">
            <h2>👑 ADMIN LOGIN</h2>
            <p>System administrators only</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("admin_login_form"):
            admin_password = st.text_input("Admin Password", type="password", placeholder="Enter admin password")
            admin_submitted = st.form_submit_button("🔑 Login as Admin", use_container_width=True)
            
            if admin_submitted:
                if admin_password == ADMIN_SECRET_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.user_type = 'admin'
                    st.session_state.username = "Admin"
                    st.success("✅ Admin login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid admin password!")
    
    st.markdown("---")
    
    # Registration Section
    st.markdown("### 📝 New User Registration")
    st.markdown("Create an account and wait for admin approval")
    
    with st.form("registration_form"):
        reg_username = st.text_input("Choose Username", placeholder="Enter username")
        reg_password = st.text_input("Choose Password", type="password", placeholder="Enter password")
        reg_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
        reg_submitted = st.form_submit_button("📝 Register", use_container_width=True)
        
        if reg_submitted:
            if reg_username and reg_password and reg_confirm:
                if reg_password == reg_confirm:
                    success, result = register_new_user(reg_username, reg_password)
                    if success:
                        secret_key = result
                        whatsapp_url = send_whatsapp_notification(reg_username, secret_key)
                        
                        st.success("✅ Registration successful! Please wait for admin approval.")
                        
                        # Show WhatsApp link
                        st.markdown(f"""
                        <div style="background: #000000; border: 2px solid #FFD700; padding: 15px; border-radius: 10px; text-align: center; margin: 10px 0;">
                            <a href="{whatsapp_url}" target="_blank" style="color: #FFD700; text-decoration: none; font-weight: bold;">
                                📱 Admin ko WhatsApp bhejein (Click Here)
                            </a>
                        </div>
                        <div class="secret-key">
                            Your Secret Key: {secret_key}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.info("Login with your credentials after admin approval!")
                    else:
                        st.error(f"❌ {result}")
                else:
                    st.error("❌ Passwords don't match!")
            else:
                st.warning("⚠️ Fill all fields!")

# ==================== MAIN APP FLOW ====================
def main():
    if not st.session_state.logged_in:
        login_page()
    elif st.session_state.user_type == 'admin':
        admin_page()
    elif st.session_state.user_type == 'pending':
        user_pending_page(st.session_state.username, st.session_state.secret_key)
    elif st.session_state.user_type == 'user':
        user_page()
    
    st.markdown('<div class="footer">Made with ❤️ by YAMRAJ | © 2025</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()