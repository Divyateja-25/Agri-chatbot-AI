import os, json, re
from dotenv import load_dotenv
load_dotenv()

from typing import Dict, Any
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

# --- 1. Setup Google Translate ---
try:
    from googletrans import Translator
    TRANSLATOR = Translator()
    HAS_GOOGLETRANS = True
except Exception:
    TRANSLATOR = None
    HAS_GOOGLETRANS = False

# --- 2. Setup Google Gemini (Updated for 2025 Models) ---
try:
    import google.generativeai as genai
    # Get key from .env
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if api_key:
        genai.configure(api_key=api_key)
        # Using the model explicitly found in your list
        model = genai.GenerativeModel('gemini-2.0-flash')
        HAS_GEMINI = True
        print("✅ DEBUG: Google Gemini (v2.0 Flash) initialized successfully.")
    else:
        print("❌ DEBUG ERROR: GOOGLE_API_KEY not found in .env file.")
        HAS_GEMINI = False
except Exception as e:
    print(f"❌ DEBUG ERROR: Could not initialize Google Gemini: {e}")
    HAS_GEMINI = False

KB_PATH = os.path.join(os.path.dirname(__file__), 'kb.json')

def load_kb():
    if not os.path.exists(KB_PATH): return {}
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    out = {}
    if isinstance(data, list):
        for entry in data:
            keys = entry.get('keywords') or []
            if isinstance(keys, str): keys = [k.strip() for k in keys.split(',') if k.strip()]
            for k in keys:
                out[k.lower()] = {
                    'en': entry.get('answer_en', ''),
                    'hi': entry.get('answer_hi', ''),
                    'ta': entry.get('answer_ta', '')
                }
    elif isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, str):
                out[k.lower()] = {'en': v}
            elif isinstance(v, dict):
                out[k.lower()] = {
                    'en': v.get('answer_en', ''),
                    'hi': v.get('answer_hi', ''),
                    'ta': v.get('answer_ta', '')
                }
    return out

KB = load_kb()

def detect_language(text: str) -> str:
    try: return detect(text)
    except Exception: return 'en'

def translate_text(text: str, dest: str) -> str:
    dest = dest[:2]
    if not HAS_GOOGLETRANS: return text
    try: return TRANSLATOR.translate(text, dest=dest).text
    except Exception: return text

def find_in_kb(message: str):
    m = message.lower()
    for k, v in KB.items():
        if k in m: return v
    tokens = re.findall(r"\w+", m)
    for k, v in KB.items():
        ktoks = re.findall(r"\w+", k)
        if any(t in ktoks for t in tokens if len(t) > 3): return v
    return None

def gemini_fallback(user_profile: Dict[str, Any], message_text: str, target_lang: str = 'en') -> str:
    if not HAS_GEMINI: 
        print("⚠️ DEBUG: Skipped Gemini call (Library not loaded).")
        return ''
    try:
        print("⏳ DEBUG: Sending request to Google Gemini...")
        
        prompt = f"""You are an expert agronomist. 
        User Profile: {user_profile}
        User Question: {message_text}
        
        Please answer the question concisely and professionally.
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        print("✅ DEBUG: Received response from Gemini!")
        
        if target_lang and target_lang != 'en' and HAS_GOOGLETRANS:
            text = translate_text(text, target_lang)
        return text
    except Exception as e:
        print(f"❌ DEBUG: Gemini API Call Failed! Error: {e}")
        return ''

def process_message(user_profile: Dict[str, Any], message_text: str) -> str:
    if not message_text or not message_text.strip():
        return 'Please ask a question.'
    
    detected = detect_language(message_text)
    if HAS_GOOGLETRANS and detected != 'en':
        try: english_text = translate_text(message_text, 'en')
        except Exception: english_text = message_text
    else:
        english_text = message_text
    
    # 1. Local KB
    kb_item = find_in_kb(english_text)
    if kb_item:
        lang = (user_profile.get('preferred_language') or detected or 'en')[:2]
        ans = kb_item.get(lang) or kb_item.get('en') or next(iter(kb_item.values()), '')
        if not ans and kb_item.get('en') and lang != 'en' and HAS_GOOGLETRANS:
            ans = translate_text(kb_item.get('en'), lang)
        return ans
    
    # 2. Gemini Fallback
    if HAS_GEMINI:
        resp = gemini_fallback(
            user_profile or {}, 
            english_text, 
            target_lang=(user_profile.get('preferred_language') or detected or 'en')[:2]
        )
        if resp: return resp
        
    return "I don't have that answer in KB. Try asking about a specific crop or pest."