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
import re

st.set_page_config(
    page_title="XMARTY AYUSH KING - Enterprise E2EE Automation",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Updated image URL
XMARTY_IMAGE_URL = "https://i.ibb.co/Rkp3VcHy/image.jpg"
NP_FILE_URL = "https://github.com/YAMRAJ275/e2e-/blob/main/np.txt"

# Professional Enterprise Theme CSS
custom_css = """
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }

    /* Main Container */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }

    .main-header p {
        color: #a0a0a0;
        font-size: 1.1rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }

    .prince-logo {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        margin-bottom: 1rem;
        border: 3px solid #fff;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        object-fit: cover;
        position: relative;
        z-index: 1;
    }

    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255,255,255,0.2);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    .stButton > button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    /* File Uploader Styles */
    .stFileUploader > div {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stFileUploader > div:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #e6e9f0 0%, #b3c7e0 100%);
    }

    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 0.5rem;
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #333;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #667eea;
        font-size: 2rem;
        font-weight: 700;
    }

    [data-testid="stMetricLabel"] {
        color: #666;
        font-weight: 500;
    }

    /* Console Output */
    .console-output {
        background: #1a1a2e;
        border-radius: 15px;
        padding: 1.5rem;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #333;
    }

    .console-line {
        padding: 0.5rem;
        margin: 0.25rem 0;
        background: rgba(255,255,255,0.05);
        border-left: 3px solid #667eea;
        font-family: 'Courier New', monospace;
    }

    /* Success/Error Boxes */
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #1a1a2e;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
    }

    .error-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
        margin-top: 2rem;
    }

    /* Card Styles */
    .card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }

    .card-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }

    /* File Info */
    .file-info {
        background: #f5f5f5;
        border-radius: 8px;
        padding: 0.5rem;
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }

    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }

    .sidebar-content {
        color: white;
        padding: 1rem;
    }

    /* Status Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    .badge-success {
        background: #84fab0;
        color: #1a1a2e;
    }

    .badge-warning {
        background: #ffd93e;
        color: #1a1a2e;
    }

    .badge-danger {
        background: #f5576c;
        color: white;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Function to parse cookies from uploaded file
def parse_cookies_file(file_content):
    """Parse cookies from various formats"""
    try:
        content = file_content.decode('utf-8')
        
        # Try to parse as JSON
        try:
            cookies_json = json.loads(content)
            if isinstance(cookies_json, list):
                # Netscape format or similar
                cookie_strings = []
                for cookie in cookies_json:
                    if 'name' in cookie and 'value' in cookie:
                        cookie_strings.append(f"{cookie['name']}={cookie['value']}")
                return '; '.join(cookie_strings)
        except:
            pass
        
        # Try to parse as Netscape format
        if '#' in content and 'HttpOnly' in content:
            lines = content.split('\n')
            cookie_strings = []
            for line in lines:
                if line and not line.startswith('#'):
                    parts = line.split('\t')
                    if len(parts) >= 7:
                        name = parts[5]
                        value = parts[6]
                        cookie_strings.append(f"{name}={value}")
            if cookie_strings:
                return '; '.join(cookie_strings)
        
        # Try to parse as simple key=value pairs
        pairs = re.findall(r'([^=]+)=([^;]+)', content)
        if pairs:
            return '; '.join([f"{k}={v}" for k, v in pairs])
        
        # If all else fails, return the content as is
        return content.strip()
    except Exception as e:
        st.error(f"Error parsing cookies file: {e}")
        return None

# Function to parse messages from uploaded file
def parse_messages_file(file_content):
    """Parse messages from file (one per line)"""
    try:
        content = file_content.decode('utf-8')
        # Split by lines and remove empty lines
        messages = [line.strip() for line in content.split('\n') if line.strip()]
        return '\n'.join(messages)
    except Exception as e:
        st.error(f"Error parsing messages file: {e}")
        return None

# Function to fetch NP file content
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_np_file():
    try:
        # Convert GitHub blob URL to raw URL
        raw_url = NP_FILE_URL.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        response = requests.get(raw_url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching NP file: {e}")
        return None

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'cookies_file_name' not in st.session_state:
    st.session_state.cookies_file_name = None
if 'messages_file_name' not in st.session_state:
    st.session_state.messages_file_name = None

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

ADMIN_UID = "Xmarty.Ayush.King.70"

def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
   
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(10)
   
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
   
    try:
        page_title = driver.title
        page_url = driver.current_url
        log_message(f'{process_id}: Page Title: {page_title}', automation_state)
        log_message(f'{process_id}: Page URL: {page_url}', automation_state)
    except Exception as e:
        log_message(f'{process_id}: Could not get page info: {e}', automation_state)
   
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
   
    log_message(f'{process_id}: Trying {len(message_input_selectors)} selectors...', automation_state)
   
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            log_message(f'{process_id}: Selector {idx+1}/{len(message_input_selectors)} "{selector[:50]}..." found {len(elements)} elements', automation_state)
           
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' ||
                               arguments[0].tagName === 'TEXTAREA' ||
                               arguments[0].tagName === 'INPUT';
                    """, element)
                   
                    if is_editable:
                        log_message(f'{process_id}: Found editable element with selector #{idx+1}', automation_state)
                       
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                       
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                       
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f'{process_id}: 👑 Found message input with text: {element_text[:50]}', automation_state)
                            return element
                        elif idx < 10:
                            log_message(f'{process_id}: 👑 Using primary selector editable element (#{idx+1})', automation_state)
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            log_message(f'{process_id}: 👑 Using fallback editable element', automation_state)
                            return element
                except Exception as e:
                    log_message(f'{process_id}: Element check failed: {str(e)[:50]}', automation_state)
                    continue
        except Exception as e:
            continue
   
    try:
        page_source = driver.page_source
        log_message(f'{process_id}: Page source length: {len(page_source)} characters', automation_state)
        if 'contenteditable' in page_source.lower():
            log_message(f'{process_id}: Page contains contenteditable elements', automation_state)
        else:
            log_message(f'{process_id}: No contenteditable elements found in page', automation_state)
    except Exception:
        pass
   
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
   
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
   
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
   
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', automation_state)
            break
   
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
   
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', automation_state)
            break
   
    try:
        from selenium.webdriver.chrome.service import Service
       
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Chrome started with detected ChromeDriver!', automation_state)
        else:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Chrome started with default driver!', automation_state)
       
        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed successfully!', automation_state)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello!'
   
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
   
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting automation...', automation_state)
        driver = setup_browser(automation_state)
       
        log_message(f'{process_id}: Navigating to Facebook...', automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
       
        if config['cookies'] and config['cookies'].strip():
            log_message(f'{process_id}: Adding cookies...', automation_state)
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
       
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            log_message(f'{process_id}: Opening conversation {chat_id}...', automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            log_message(f'{process_id}: Opening messages...', automation_state)
            driver.get('https://www.facebook.com/messages')
       
        time.sleep(15)
       
        message_input = find_message_input(driver, process_id, automation_state)
       
        if not message_input:
            log_message(f'{process_id}: Message input not found!', automation_state)
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
       
        delay = int(config['delay'])
        messages_sent = 0
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
       
        if not messages_list:
            messages_list = ['Hello!']
       
        while automation_state.running:
            base_message = get_next_message(messages_list, automation_state)
           
            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
           
            try:
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];
                   
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                   
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }
                   
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                """, message_input, message_to_send)
               
                time.sleep(1)
               
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                   
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
               
                if sent == 'button_not_found':
                    log_message(f'{process_id}: Send button not found, using Enter key...', automation_state)
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                       
                        const events = [
                            new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                        ];
                       
                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
                    log_message(f'{process_id}: 👑 Sent via Enter: "{message_to_send[:30]}..."', automation_state)
                else:
                    log_message(f'{process_id}: 👑 Sent via button: "{message_to_send[:30]}..."', automation_state)
               
                messages_sent += 1
                automation_state.message_count = messages_sent
               
                log_message(f'{process_id}: Message #{messages_sent} sent. Waiting {delay}s...', automation_state)
                time.sleep(delay)
               
            except Exception as e:
                log_message(f'{process_id}: Send error: {str(e)[:100]}', automation_state)
                time.sleep(5)
       
        log_message(f'{process_id}: Automation stopped. Total messages: {messages_sent}', automation_state)
        return messages_sent
       
    except Exception as e:
        log_message(f'{process_id}: Fatal error: {str(e)}', automation_state)
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f'{process_id}: Browser closed', automation_state)
            except:
                pass

def send_admin_notification(user_config, username, automation_state, user_id):
    driver = None
    try:
        log_message(f"ADMIN-NOTIFY: Preparing admin notification...", automation_state)
       
        admin_e2ee_thread_id = db.get_admin_e2ee_thread_id(user_id)
       
        if admin_e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: Using saved admin thread: {admin_e2ee_thread_id}", automation_state)
       
        driver = setup_browser(automation_state)
       
        log_message(f"ADMIN-NOTIFY: Navigating to Facebook...", automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
       
        if user_config['cookies'] and user_config['cookies'].strip():
            log_message(f"ADMIN-NOTIFY: Adding cookies...", automation_state)
            cookie_array = user_config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
       
        user_chat_id = user_config.get('chat_id', '')
        admin_found = False
        e2ee_thread_id = admin_e2ee_thread_id
        chat_type = 'REGULAR'
       
        if e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: Opening saved admin conversation...", automation_state)
           
            if '/e2ee/' in str(e2ee_thread_id) or admin_e2ee_thread_id:
                conversation_url = f'https://www.facebook.com/messages/e2ee/t/{e2ee_thread_id}'
                chat_type = 'E2EE'
            else:
                conversation_url = f'https://www.facebook.com/messages/t/{e2ee_thread_id}'
                chat_type = 'REGULAR'
           
            log_message(f"ADMIN-NOTIFY: Opening {chat_type} conversation: {conversation_url}", automation_state)
            driver.get(conversation_url)
            time.sleep(8)
            admin_found = True
       
        if not admin_found or not e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: Searching for admin UID: {ADMIN_UID}...", automation_state)
           
            try:
                profile_url = f'https://www.facebook.com/{ADMIN_UID}'
                log_message(f"ADMIN-NOTIFY: Opening admin profile: {profile_url}", automation_state)
                driver.get(profile_url)
                time.sleep(8)
               
                message_button_selectors = [
                    'div[aria-label*="Message" i]',
                    'a[aria-label*="Message" i]',
                    'div[role="button"]:has-text("Message")',
                    'a[role="button"]:has-text("Message")',
                    '[data-testid*="message"]'
                ]
               
                message_button = None
                for selector in message_button_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            for elem in elements:
                                text = elem.text.lower() if elem.text else ""
                                aria_label = elem.get_attribute('aria-label') or ""
                                if 'message' in text or 'message' in aria_label.lower():
                                    message_button = elem
                                    log_message(f"ADMIN-NOTIFY: Found message button: {selector}", automation_state)
                                    break
                            if message_button:
                                break
                    except:
                        continue
               
                if message_button:
                    log_message(f"ADMIN-NOTIFY: Clicking message button...", automation_state)
                    driver.execute_script("arguments[0].click();", message_button)
                    time.sleep(8)
                   
                    current_url = driver.current_url
                    log_message(f"ADMIN-NOTIFY: Redirected to: {current_url}", automation_state)
                   
                    if '/messages/t/' in current_url or '/e2ee/t/' in current_url:
                        if '/e2ee/t/' in current_url:
                            e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                            chat_type = 'E2EE'
                            log_message(f"ADMIN-NOTIFY: 👑 Found E2EE conversation: {e2ee_thread_id}", automation_state)
                        else:
                            e2ee_thread_id = current_url.split('/messages/t/')[-1].split('?')[0].split('/')[0]
                            chat_type = 'REGULAR'
                            log_message(f"ADMIN-NOTIFY: 👑 Found REGULAR conversation: {e2ee_thread_id}", automation_state)
                       
                        if e2ee_thread_id and e2ee_thread_id != user_chat_id and user_id:
                            current_cookies = user_config.get('cookies', '')
                            db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, chat_type)
                            admin_found = True
                    else:
                        log_message(f"ADMIN-NOTIFY: Message button didn't redirect to messages page", automation_state)
                else:
                    log_message(f"ADMIN-NOTIFY: Could not find message button on profile", automation_state)
           
            except Exception as e:
                log_message(f"ADMIN-NOTIFY: Profile approach failed: {str(e)[:100]}", automation_state)
           
            if not admin_found or not e2ee_thread_id:
                log_message(f"ADMIN-NOTIFY: ❌❌ Could not find admin via search, trying DIRECT MESSAGE approach...", automation_state)
               
                try:
                    profile_url = f'https://www.facebook.com/messages/new'
                    log_message(f"ADMIN-NOTIFY: Opening new message page...", automation_state)
                    driver.get(profile_url)
                    time.sleep(8)
                   
                    search_box = None
                    search_selectors = [
                        'input[aria-label*="To:" i]',
                        'input[placeholder*="Type a name" i]',
                        'input[type="text"]'
                    ]
                   
                    for selector in search_selectors:
                        try:
                            search_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            if search_elements:
                                for elem in search_elements:
                                    if elem.is_displayed():
                                        search_box = elem
                                        log_message(f"ADMIN-NOTIFY: Found 'To:' box with: {selector}", automation_state)
                                        break
                                if search_box:
                                    break
                        except:
                            continue
                   
                    if search_box:
                        log_message(f"ADMIN-NOTIFY: Typing admin UID in new message...", automation_state)
                        driver.execute_script("""
                            arguments[0].focus();
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                        """, search_box, ADMIN_UID)
                        time.sleep(5)
                       
                        result_elements = driver.find_elements(By.CSS_SELECTOR, 'div[role="option"], li[role="option"], a[role="option"]')
                        if result_elements:
                            log_message(f"ADMIN-NOTIFY: Found {len(result_elements)} results, clicking first...", automation_state)
                            driver.execute_script("arguments[0].click();", result_elements[0])
                            time.sleep(8)
                           
                            current_url = driver.current_url
                            if '/messages/t/' in current_url or '/e2ee/t/' in current_url:
                                if '/e2ee/t/' in current_url:
                                    e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                                    chat_type = 'E2EE'
                                    log_message(f"ADMIN-NOTIFY: 👑 Direct message opened E2EE: {e2ee_thread_id}", automation_state)
                                else:
                                    e2ee_thread_id = current_url.split('/messages/t/')[-1].split('?')[0].split('/')[0]
                                    chat_type = 'REGULAR'
                                    log_message(f"ADMIN-NOTIFY: 👑 Direct message opened REGULAR chat: {e2ee_thread_id}", automation_state)
                               
                                if e2ee_thread_id and e2ee_thread_id != user_chat_id and user_id:
                                    current_cookies = user_config.get('cookies', '')
                                    db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, chat_type)
                                    admin_found = True
                except Exception as e:
                    log_message(f"ADMIN-NOTIFY: Direct message approach failed: {str(e)[:100]}", automation_state)
       
        if not admin_found or not e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: ❌ ALL APPROACHES FAILED - Could not find/open admin conversation", automation_state)
            return
       
        conversation_type = "E2EE" if "e2ee" in driver.current_url else "REGULAR"
        log_message(f"ADMIN-NOTIFY: 👑 Successfully opened {conversation_type} conversation with admin", automation_state)
       
        message_input = find_message_input(driver, 'ADMIN-NOTIFY', automation_state)
       
        if message_input:
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conversation_type = "E2EE 👑" if "e2ee" in driver.current_url.lower() else "Regular 👑"
            notification_msg = f"👑 New User Started Automation\n\n👑 Username: {username}\n👑 Time: {current_time}\n👑 Chat Type: {conversation_type}\n👑 Thread ID: {e2ee_thread_id if e2ee_thread_id else 'N/A'}"
           
            log_message(f"ADMIN-NOTIFY: Typing notification message...", automation_state)
            driver.execute_script("""
                const element = arguments[0];
                const message = arguments[1];
               
                element.scrollIntoView({behavior: 'smooth', block: 'center'});
                element.focus();
                element.click();
               
                if (element.tagName === 'DIV') {
                    element.textContent = message;
                    element.innerHTML = message;
                } else {
                    element.value = message;
                }
               
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
            """, message_input, notification_msg)
           
            time.sleep(1)
           
            log_message(f"ADMIN-NOTIFY: Trying to send message...", automation_state)
            send_result = driver.execute_script("""
                const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
               
                for (let btn of sendButtons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        return 'button_clicked';
                    }
                }
                return 'button_not_found';
            """)
           
            if send_result == 'button_not_found':
                log_message(f"ADMIN-NOTIFY: Send button not found, using Enter key...", automation_state)
                driver.execute_script("""
                    const element = arguments[0];
                    element.focus();
                   
                    const events = [
                        new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                        new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                        new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                    ];
                   
                    events.forEach(event => element.dispatchEvent(event));
                """, message_input)
                log_message(f"ADMIN-NOTIFY: 👑 Sent via Enter key", automation_state)
            else:
                log_message(f"ADMIN-NOTIFY: 👑 Send button clicked", automation_state)
           
            time.sleep(2)
        else:
            log_message(f"ADMIN-NOTIFY: ❌ Failed to find message input", automation_state)
           
    except Exception as e:
        log_message(f"ADMIN-NOTIFY: ❌ Error sending notification: {str(e)}", automation_state)
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f"ADMIN-NOTIFY: Browser closed", automation_state)
            except:
                pass

def run_automation_with_notification(user_config, username, automation_state, user_id):
    send_admin_notification(user_config, username, automation_state, user_id)
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
   
    if automation_state.running:
        return
   
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
   
    db.set_automation_running(user_id, True)
   
    username = db.get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

def login_page():
    st.markdown(f"""
    <div class="main-header">
        <img src="{XMARTY_IMAGE_URL}" class="prince-logo">
        <h1>XMARTY AYUSH KING</h1>
        <p>Enterprise E2EE Automation Platform</p>
    </div>
    """, unsafe_allow_html=True)
   
    col1, col2, col3 = st.columns([1, 2, 1])
   
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header">🔐 Secure Login</div>', unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["📱 Login", "✨ Sign Up"])
            
            with tab1:
                username = st.text_input("Username", key="login_username", placeholder="Enter your username")
                password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
                
                if st.button("Login", key="login_btn", use_container_width=True):
                    if username and password:
                        user_id = db.verify_user(username, password)
                        if user_id:
                            st.session_state.logged_in = True
                            st.session_state.user_id = user_id
                            st.session_state.username = username
                            
                            should_auto_start = db.get_automation_running(user_id)
                            if should_auto_start:
                                user_config = db.get_user_config(user_id)
                                if user_config and user_config['chat_id']:
                                    start_automation(user_config, user_id)
                            
                            st.success(f"✅ Welcome back, {username}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password!")
                    else:
                        st.warning("⚠️ Please enter both username and password")
            
            with tab2:
                new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
                new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
                confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
                
                if st.button("Create Account", key="signup_btn", use_container_width=True):
                    if new_username and new_password and confirm_password:
                        if new_password == confirm_password:
                            success, message = db.create_user(new_username, new_password)
                            if success:
                                st.success(f"✅ {message} Please login now!")
                            else:
                                st.error(f"❌ {message}")
                        else:
                            st.error("❌ Passwords do not match!")
                    else:
                        st.warning("⚠️ Please fill all fields")
            
            st.markdown('</div>', unsafe_allow_html=True)

def main_app():
    st.markdown(f"""
    <div class="main-header">
        <img src="{XMARTY_IMAGE_URL}" class="prince-logo">
        <h1>XMARTY AYUSH KING</h1>
        <p>Enterprise E2EE Automation Platform</p>
    </div>
    """, unsafe_allow_html=True)
   
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = db.get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                start_automation(user_config, st.session_state.user_id)
   
    # Sidebar
    with st.sidebar:
        st.markdown("### 👑 User Profile")
        st.markdown(f"**Username:** {st.session_state.username}")
        st.markdown(f"**User ID:** `{st.session_state.user_id[:8]}...`" if st.session_state.user_id else "**User ID:** N/A")
        
        st.markdown("---")
        
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", st.session_state.automation_state.message_count)
        with col2:
            status = "🟢" if st.session_state.automation_state.running else "🔴"
            st.metric("Status", status)
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            if st.session_state.automation_state.running:
                stop_automation(st.session_state.user_id)
            
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.automation_running = False
            st.session_state.auto_start_checked = False
            st.rerun()
    
    # Main Content
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        tab1, tab2 = st.tabs(["⚙️ Configuration", "🤖 Automation Control"])
        
        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header">📋 Campaign Settings</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'],
                                       placeholder="e.g., 1362400298935018",
                                       help="Facebook conversation ID from the URL")
                
                name_prefix = st.text_input("Message Prefix", value=user_config['name_prefix'],
                                           placeholder="e.g., [E2EE]",
                                           help="Prefix to add before each message")
            
            with col2:
                delay = st.number_input("Delay (seconds)", min_value=1, max_value=300,
                                       value=user_config['delay'],
                                       help="Wait time between messages")
                
                st.markdown("### 📁 File Uploads")
                st.info("Upload files instead of copy-pasting")
            
            st.markdown("---")
            
            # Cookies File Upload
            st.markdown("### 🍪 Cookies File")
            cookies_file = st.file_uploader(
                "Upload cookies file (txt, json, netscape format)",
                type=['txt', 'json', 'cookie'],
                key="cookies_uploader",
                help="Upload your Facebook cookies file. Supported formats: Netscape, JSON, key=value pairs"
            )
            
            if cookies_file:
                cookies_content = parse_cookies_file(cookies_file.getvalue())
                if cookies_content:
                    st.session_state.cookies_file_name = cookies_file.name
                    st.success(f"✅ Cookies loaded from: {cookies_file.name}")
                    st.markdown(f'<div class="file-info">📄 {len(cookies_content)} characters loaded</div>', unsafe_allow_html=True)
                else:
                    st.error("❌ Failed to parse cookies file")
            else:
                cookies_content = user_config['cookies']
            
            st.markdown("---")
            
            # Messages File Upload
            st.markdown("### 📝 Messages File")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                messages_file = st.file_uploader(
                    "Upload messages file (txt, one per line)",
                    type=['txt'],
                    key="messages_uploader",
                    help="Upload a text file with one message per line"
                )
            with col2:
                if st.button("📥 Load NP File", use_container_width=True):
                    with st.spinner("Loading NP file..."):
                        np_content = fetch_np_file()
                        if np_content:
                            st.session_state['messages_content'] = np_content
                            st.success("✅ NP file loaded successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to load NP file")
            
            if messages_file:
                messages_content = parse_messages_file(messages_file.getvalue())
                if messages_content:
                    st.session_state.messages_file_name = messages_file.name
                    message_lines = len(messages_content.split('\n'))
                    st.success(f"✅ Messages loaded from: {messages_file.name}")
                    st.markdown(f'<div class="file-info">📄 {message_lines} messages loaded</div>', unsafe_allow_html=True)
                    
                    # Preview first few messages
                    with st.expander("📋 Preview Messages"):
                        preview_lines = messages_content.split('\n')[:5]
                        for i, line in enumerate(preview_lines, 1):
                            st.text(f"{i}. {line[:50]}{'...' if len(line) > 50 else ''}")
                        if len(messages_content.split('\n')) > 5:
                            st.text(f"... and {len(messages_content.split('\n')) - 5} more")
                else:
                    st.error("❌ Failed to parse messages file")
            elif 'messages_content' in st.session_state:
                messages_content = st.session_state['messages_content']
                message_lines = len(messages_content.split('\n'))
                st.info(f"📄 NP file loaded with {message_lines} messages")
                
                # Preview first few messages
                with st.expander("📋 Preview NP File Messages"):
                    preview_lines = messages_content.split('\n')[:5]
                    for i, line in enumerate(preview_lines, 1):
                        st.text(f"{i}. {line[:50]}{'...' if len(line) > 50 else ''}")
                    if message_lines > 5:
                        st.text(f"... and {message_lines - 5} more")
            else:
                messages_content = user_config['messages']
            
            st.markdown("---")
            
            if st.button("💾 Save Configuration", use_container_width=True):
                final_cookies = cookies_content if 'cookies_content' in locals() and cookies_content else user_config['cookies']
                final_messages = messages_content if 'messages_content' in locals() and messages_content else user_config['messages']
                
                db.update_user_config(
                    st.session_state.user_id,
                    chat_id,
                    name_prefix,
                    delay,
                    final_cookies,
                    final_messages
                )
                
                # Clear temporary session state
                if 'messages_content' in st.session_state:
                    del st.session_state['messages_content']
                
                st.success("✅ Configuration saved successfully!")
                st.balloons()
                time.sleep(1)
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header">🎮 Automation Control Panel</div>', unsafe_allow_html=True)
            
            user_config = db.get_user_config(st.session_state.user_id)
            
            # Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Messages Sent", st.session_state.automation_state.message_count)
            with col2:
                status = "🟢 Running" if st.session_state.automation_state.running else "🔴 Stopped"
                st.metric("Status", status)
            with col3:
                st.metric("Chat ID", user_config['chat_id'][:8] + "..." if user_config['chat_id'] else "Not Set")
            with col4:
                message_count = len(user_config['messages'].split('\n')) if user_config['messages'] else 0
                st.metric("Total Messages", message_count)
            
            st.markdown("---")
            
            # Control Buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("▶️ Start Automation", disabled=st.session_state.automation_state.running, use_container_width=True):
                    if user_config['chat_id']:
                        if user_config['messages']:
                            start_automation(user_config, st.session_state.user_id)
                            st.success("✅ Automation started!")
                            st.rerun()
                        else:
                            st.error("❌ Please upload messages file first!")
                    else:
                        st.error("❌ Please set Chat ID in Configuration first!")
            
            with col2:
                if st.button("⏸️ Pause Automation", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.warning("⚠️ Automation paused!")
                    st.rerun()
            
            with col3:
                if st.button("🔄 Reset Counter", use_container_width=True):
                    st.session_state.automation_state.message_count = 0
                    st.rerun()
            
            st.markdown("---")
            
            # Console Output
            if st.session_state.automation_state.logs:
                st.markdown("### 📟 Live Console Output")
                
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-30:]:
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
                
                st.markdown(logs_html, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Refresh Logs", use_container_width=True):
                        st.rerun()
                with col2:
                    if st.button("🗑️ Clear Logs", use_container_width=True):
                        st.session_state.automation_state.logs = []
                        st.rerun()
            else:
                st.info("📝 No logs available. Start automation to see console output.")
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ No configuration found. Please refresh the page!")

# Main app flow
if not st.session_state.logged_in:
    login_page()
else:
    main_app()

st.markdown('<div class="footer">© 2025 XMARTY AYUSH KING - Enterprise E2EE Automation Platform. All rights reserved.</div>', unsafe_allow_html=True)