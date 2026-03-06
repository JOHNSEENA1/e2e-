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
import psutil
from datetime import datetime

st.set_page_config(
    page_title="E2E RISHU SERVER",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
custom_css = """
<style>
    /* Clean font */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #000428, #004e92);
    }

    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        border: 2px solid #00ffff;
    }

    /* Header with RISHU name */
    .main-header {
        background: linear-gradient(135deg, #000428, #004e92);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
        border: 3px solid #00ffff;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        color: #00ffff;
        text-shadow: 0 0 20px #00ffff;
    }
    
    .main-header p {
        color: white;
        font-size: 1.2rem;
        margin: 5px 0 0 0;
    }

    /* E2E Server Badge */
    .server-badge {
        display: inline-block;
        background: #00ffff;
        color: black;
        padding: 5px 20px;
        border-radius: 30px;
        font-weight: bold;
        margin-top: 10px;
        animation: glow 2s infinite;
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px #00ffff; }
        50% { box-shadow: 0 0 20px #00ffff; }
        100% { box-shadow: 0 0 5px #00ffff; }
    }

    /* Uptime Engine - Live Status */
    .uptime-engine {
        background: linear-gradient(135deg, #000428, #001f3f);
        border: 3px solid #00ffff;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
    }
    
    .uptime-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
        border-bottom: 1px solid #00ffff;
        padding-bottom: 10px;
    }
    
    .uptime-header h2 {
        color: #00ffff;
        margin: 0;
        font-size: 1.8rem;
        text-shadow: 0 0 10px #00ffff;
    }
    
    .live-badge {
        background: #00ffff;
        color: black;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .uptime-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 15px;
    }
    
    .uptime-card {
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid #00ffff;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
    }
    
    .uptime-card .label {
        color: #00ffff;
        font-size: 0.9rem;
        text-transform: uppercase;
    }
    
    .uptime-card .value {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .live-log-container {
        background: #000000;
        border: 2px solid #00ffff;
        border-radius: 10px;
        padding: 10px;
        max-height: 200px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
    }
    
    .live-log-line {
        color: #00ff00;
        padding: 3px 8px;
        border-bottom: 1px solid #333;
        font-size: 12px;
    }
    
    .live-log-line.success { color: #00ff00; }
    .live-log-line.error { color: #ff4444; }
    .live-log-line.warning { color: #ffff00; }
    .live-log-line.send { color: #00ffff; }

    /* Direct Access - No Login Box */
    .direct-access {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        border: none;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
        color: white;
        font-weight: bold;
    }

    /* Touch Upload Button */
    .touch-upload {
        background: linear-gradient(135deg, #00ffff, #000428);
        border: none;
        border-radius: 50px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        cursor: pointer;
        transition: all 0.3s;
        border: 2px solid white;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    
    .touch-upload:hover {
        transform: scale(1.02);
        box-shadow: 0 0 40px rgba(0, 255, 255, 0.8);
    }
    
    .touch-upload h3 {
        color: white;
        margin: 0;
        font-size: 1.8rem;
        text-shadow: 0 0 10px black;
    }
    
    .touch-upload p {
        color: white;
        margin: 5px 0 0 0;
        font-size: 1rem;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.3s;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }

    /* START Button */
    div[data-testid="column"]:nth-of-type(1) .stButton>button {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        color: white;
    }
    
    /* STOP Button */
    div[data-testid="column"]:nth-of-type(2) .stButton>button {
        background: linear-gradient(135deg, #eb3349, #f45c43);
        color: white;
    }
    
    /* CLOSE ALL Button */
    div[data-testid="column"]:nth-of-type(3) .stButton>button {
        background: linear-gradient(135deg, #f12711, #f5af19);
        color: white;
        animation: pulse 2s infinite;
    }

    /* Input Fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #00ffff;
        padding: 12px;
        font-size: 1rem;
        color: black !important;
        background: white;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #000428;
        box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.3);
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00ffff;
        font-size: 2rem;
        font-weight: 700;
        text-shadow: 0 0 10px #00ffff;
    }
    
    [data-testid="stMetricLabel"] {
        color: #000428;
        font-weight: 600;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: white;
        padding: 20px;
        font-size: 1rem;
        border-top: 2px solid #00ffff;
        margin-top: 30px;
    }
    
    .rishu-signature {
        color: #00ffff;
        font-weight: bold;
        font-size: 1.2rem;
        text-shadow: 0 0 10px #00ffff;
    }
    
    /* Console Output */
    .console-output {
        background: #1e1e2f;
        border-radius: 10px;
        padding: 15px;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        max-height: 400px;
        overflow-y: auto;
        margin-top: 20px;
        border: 2px solid #00ffff;
    }

    .console-line {
        border-bottom: 1px solid #333;
        padding: 5px 10px;
        margin: 3px 0;
        font-family: 'Courier New', monospace;
        color: #00ff00;
    }
    
    .console-line.success { color: #00ff00; }
    .console-line.error { color: #ff4444; }
    .console-line.warning { color: #ffff00; }
    .console-line.send { color: #00ffff; }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ==================== CONSTANTS ====================
UPTIME_START = datetime.now()

# ==================== SESSION STATE ====================
if 'user_id' not in st.session_state:
    # Create default user automatically - NO LOGIN REQUIRED
    db.init_database()
    success, _ = db.create_user("rishu", "rishu123")
    if success:
        st.session_state.user_id = db.verify_user("rishu", "rishu123")
    else:
        st.session_state.user_id = 1  # Fallback
    
if 'username' not in st.session_state:
    st.session_state.username = "RISHU"
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
if 'cpu_usage' not in st.session_state:
    st.session_state.cpu_usage = 0
if 'memory_usage' not in st.session_state:
    st.session_state.memory_usage = 0

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

# ==================== UPTIME ENGINE FUNCTIONS ====================
def get_uptime():
    """Get system uptime"""
    delta = datetime.now() - UPTIME_START
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

def get_system_stats():
    """Get system CPU and memory usage"""
    try:
        st.session_state.cpu_usage = psutil.cpu_percent(interval=1)
        st.session_state.memory_usage = psutil.virtual_memory().percent
    except:
        st.session_state.cpu_usage = 0
        st.session_state.memory_usage = 0

# ==================== LOGGING FUNCTION ====================
def log_message(msg, msg_type="info", automation_state=None):
    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    
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

# ==================== TOUCH UPLOAD FUNCTION ====================
def touch_upload_messages():
    """Single touch to upload messages from np.txt"""
    try:
        if os.path.exists("np.txt"):
            with open("np.txt", 'r', encoding='utf-8') as f:
                messages = f.read()
            st.session_state.messages_content = messages
            line_count = len(messages.splitlines())
            log_message(f"📥 Touch upload: {line_count} messages loaded", "load")
            return True, f"✅ Loaded {line_count} messages"
        else:
            log_message("❌ np.txt not found", "error")
            return False, "❌ np.txt file not found!"
    except Exception as e:
        log_message(f"❌ Upload error: {str(e)}", "error")
        return False, f"❌ Error: {str(e)}"

# ==================== AUTOMATION FUNCTIONS ====================
def setup_browser(automation_state=None):
    """Setup Chrome browser"""
    log_message('Setting up Chrome browser...', "info", automation_state)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
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
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Browser started!', "success", automation_state)
        except:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Browser started with default driver!', "success", automation_state)
        
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', "error", automation_state)
        raise error

def find_message_input(driver, process_id, automation_state=None):
    """Find message input"""
    log_message(f'Finding message input...', "info", automation_state)
    time.sleep(5)
    
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea'
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

def send_messages(config, automation_state, user_id, process_id='RISHU'):
    """Send messages"""
    driver = None
    try:
        automation_state.start_time = datetime.now()
        
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        total_msgs = len(messages_list)
        automation_state.total_messages = total_msgs
        
        log_message(f'📥 Loaded: {total_msgs} messages', "load", automation_state)
        log_message(f'Starting RISHU automation...', "info", automation_state)
        
        delay = int(config['delay'])
        log_message(f'⏱️ Delay: {delay}s', "info", automation_state)
        
        driver = setup_browser(automation_state)
        automation_state.driver = driver
        
        log_message(f'Opening Facebook...', "info", automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(5)
        
        if config['cookies']:
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
                log_message(f'✅ Cookies added', "success", automation_state)
            except:
                pass
        
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            automation_state.current_chat_id = chat_id
            log_message(f'Opening chat {chat_id}...', "info", automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
            time.sleep(8)
        
        message_input = find_message_input(driver, process_id, automation_state)
        if not message_input:
            log_message(f'❌ No message input!', "error", automation_state)
            return 0
        
        messages_sent = 0
        for i, message in enumerate(messages_list):
            if not automation_state.running:
                break
            
            try:
                if config['name_prefix']:
                    full_message = f"{config['name_prefix']} {message}"
                else:
                    full_message = message
                
                message_input.clear()
                message_input.send_keys(full_message)
                time.sleep(1)
                message_input.send_keys(Keys.RETURN)
                
                messages_sent += 1
                automation_state.message_count = messages_sent
                
                log_message(f"📤 [{chat_id}] {messages_sent}/{total_msgs}", "send", automation_state)
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'❌ Send error', "error", automation_state)
                time.sleep(5)
        
        log_message(f'✅ Completed: {messages_sent} messages', "success", automation_state)
        automation_state.running = False
        return messages_sent
        
    except Exception as e:
        log_message(f'❌ Fatal: {str(e)}', "error", automation_state)
        automation_state.running = False
        return 0
    finally:
        if driver:
            driver.quit()

def start_automation(user_config, user_id):
    if st.session_state.automation_state.running:
        return
    st.session_state.automation_state.running = True
    st.session_state.automation_state.message_count = 0
    st.session_state.automation_state.logs = []
    thread = threading.Thread(target=send_messages, args=(user_config, st.session_state.automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    log_message("⏹️ Stopped by user", "warning", st.session_state.automation_state)

def close_all_tasks():
    with st.spinner("🧹 Cleaning up..."):
        if st.session_state.automation_state.running:
            st.session_state.automation_state.running = False
        if hasattr(st.session_state.automation_state, 'driver') and st.session_state.automation_state.driver:
            try:
                st.session_state.automation_state.driver.quit()
            except:
                pass
        try:
            os.system("pkill -f chrome")
            os.system("pkill -f chromedriver")
        except:
            pass
        st.session_state.automation_state.message_count = 0
        st.session_state.automation_state.logs = []
        gc.collect()
        time.sleep(2)
        st.success("✅ All tasks closed!")

# ==================== UPTIME ENGINE DISPLAY ====================
def display_uptime_engine():
    """Display live uptime engine at top"""
    get_system_stats()
    
    uptime_html = f'''
    <div class="uptime-engine">
        <div class="uptime-header">
            <h2>⚡ E2E RISHU SERVER ⚡</h2>
            <span class="live-badge">🔴 LIVE</span>
        </div>
        
        <div class="uptime-grid">
            <div class="uptime-card">
                <div class="label">Server Uptime</div>
                <div class="value">{get_uptime()}</div>
            </div>
            <div class="uptime-card">
                <div class="label">CPU Usage</div>
                <div class="value">{st.session_state.cpu_usage}%</div>
            </div>
            <div class="uptime-card">
                <div class="label">Memory</div>
                <div class="value">{st.session_state.memory_usage}%</div>
            </div>
            <div class="uptime-card">
                <div class="label">Messages Sent</div>
                <div class="value">{st.session_state.automation_state.message_count}</div>
            </div>
        </div>
        
        <div class="live-log-container">
    '''
    
    # Add last 10 logs
    if st.session_state.automation_state.logs:
        for log in st.session_state.automation_state.logs[-10:]:
            log_class = "live-log-line"
            if "✅" in log:
                log_class += " success"
            elif "❌" in log:
                log_class += " error"
            elif "⚠️" in log:
                log_class += " warning"
            elif "📤" in log:
                log_class += " send"
            uptime_html += f'<div class="{log_class}">{log}</div>'
    else:
        uptime_html += '<div class="live-log-line">⏳ Waiting for activity...</div>'
    
    uptime_html += '''
        </div>
    </div>
    '''
    
    st.markdown(uptime_html, unsafe_allow_html=True)

# ==================== MAIN APP - DIRECT ACCESS ====================
def main():
    # Header with RISHU name
    st.markdown("""
    <div class="main-header">
        <h1>🚀 E2E RISHU SERVER</h1>
        <p>Direct Access - No Login Required</p>
        <span class="server-badge">🔓 OPEN FOR ALL</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Display Uptime Engine at TOP
    display_uptime_engine()
    
    # DIRECT ACCESS - NO LOGIN REQUIRED
    st.markdown('<div class="direct-access">✅ Welcome RISHU! You have direct access to the server</div>', unsafe_allow_html=True)
    
    # Get user config
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        tab1, tab2 = st.tabs(["⚙️ Configuration", "🤖 Automation"])
        
        with tab1:
            st.markdown("### ⚙️ Configuration")
            
            chat_id = st.text_input("Chat ID", value=user_config['chat_id'], placeholder="e.g., 1362400298935018")
            name_prefix = st.text_input("Prefix", value=user_config['name_prefix'], placeholder="e.g., [RISHU]")
            delay = st.number_input("Delay (seconds)", 1, 300, user_config['delay'])
            cookies = st.text_area("Facebook Cookies", value=user_config['cookies'], height=150, 
                                  placeholder="c_user=xxxx; xs=xxxx; fr=xxxx;")
            
            # TOUCH UPLOAD BUTTON
            st.markdown("### 📁 Touch Upload Messages")
            
            # Hidden file uploader
            uploaded_file = st.file_uploader("", type=['txt'], key="touch_upload", label_visibility="collapsed")
            
            if uploaded_file:
                messages = uploaded_file.read().decode('utf-8')
                st.session_state.messages_content = messages
                line_count = len(messages.splitlines())
                st.success(f"✅ Touched! {line_count} messages loaded from {uploaded_file.name}")
                log_message(f"📥 Touch uploaded: {line_count} messages", "load")
                time.sleep(1)
                st.rerun()
            
            # Big Touch Button
            st.markdown("""
            <div class="touch-upload" onclick="document.querySelector('input[type=file]').click()">
                <h3>👆 TOUCH HERE TO UPLOAD</h3>
                <p>Click or touch anywhere on this button to load messages from np.txt</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Messages preview
            messages_to_show = st.session_state.get('messages_content', user_config['messages'])
            line_count = len(messages_to_show.split('\n')) if messages_to_show else 0
            
            preview = messages_to_show[:500] + "..." if len(messages_to_show) > 500 else messages_to_show
            st.text_area("Messages Preview", value=preview, height=150, disabled=True)
            st.info(f"📊 Total messages: {line_count} lines")
            
            if st.button("💾 Save Configuration", use_container_width=True):
                final_messages = st.session_state.get('messages_content', user_config['messages'])
                if db.update_user_config(st.session_state.user_id, chat_id, name_prefix, delay, cookies, final_messages):
                    st.success("✅ Configuration saved successfully!")
                    log_message("💾 Configuration saved", "success")
                    st.rerun()
                else:
                    st.error("❌ Failed to save configuration")
        
        with tab2:
            st.markdown("### 🤖 Automation Control")
            
            # Status metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Messages Sent", st.session_state.automation_state.message_count)
            with col2:
                status = "🟢 RUNNING" if st.session_state.automation_state.running else "🔴 STOPPED"
                st.metric("Status", status)
            with col3:
                chat_display = user_config['chat_id'][:10] + "..." if user_config['chat_id'] and len(user_config['chat_id']) > 10 else user_config['chat_id'] or "Not Set"
                st.metric("Chat ID", chat_display)
            
            st.markdown("---")
            
            # Control buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                start_disabled = st.session_state.automation_state.running or not user_config['chat_id'] or not user_config['cookies']
                if st.button("▶️ START AUTOMATION", disabled=start_disabled, use_container_width=True):
                    if user_config['chat_id'] and user_config['cookies']:
                        start_automation(user_config, st.session_state.user_id)
                        st.success("✅ Automation started!")
                        log_message("▶️ Automation started", "success")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Please set Chat ID and Cookies first!")
            
            with col2:
                if st.button("⏹️ STOP AUTOMATION", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.warning("⏹️ Automation stopped!")
                    time.sleep(1)
                    st.rerun()
            
            with col3:
                if st.button("🗑️ CLOSE ALL TASKS", use_container_width=True):
                    st.session_state.show_close_confirmation = True
            
            # Confirmation dialog for CLOSE ALL
            if st.session_state.show_close_confirmation:
                st.warning("⚠️ Are you sure you want to close ALL tasks? This will stop automation and close browser!")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ YES, CLOSE ALL", use_container_width=True):
                        st.session_state.show_close_confirmation = False
                        close_all_tasks()
                        st.rerun()
                with col2:
                    if st.button("❌ NO, CANCEL", use_container_width=True):
                        st.session_state.show_close_confirmation = False
                        st.rerun()
            
            # Auto-refresh when running
            if st.session_state.automation_state.running:
                time.sleep(2)
                st.rerun()
            
            # Full logs at bottom
            if st.session_state.automation_state.logs:
                st.markdown("### 📟 Complete Log History")
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-50:]:
                    log_class = ""
                    if "✅" in log:
                        log_class = 'success'
                    elif "❌" in log:
                        log_class = 'error'
                    elif "📤" in log:
                        log_class = 'send'
                    logs_html += f'<div class="console-line {log_class}">{log}</div>'
                logs_html += '</div>'
                st.markdown(logs_html, unsafe_allow_html=True)
    else:
        st.error("❌ Configuration not found. Please check database.")

# ==================== RUN ====================
if __name__ == "__main__":
    main()
    st.markdown('<div class="footer">⚡ <span class="rishu-signature">E2E RISHU SERVER</span> ⚡ | Direct Access | No Approval Required</div>', unsafe_allow_html=True)
