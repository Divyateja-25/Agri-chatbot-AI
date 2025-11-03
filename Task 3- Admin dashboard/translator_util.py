# translator_util.py
from deep_translator import GoogleTranslator

def translate_text(text, dest="en"):
    """
    Translates text to the destination language.
    """
    try:
        # Use GoogleTranslator from the deep-translator library
        return GoogleTranslator(source='auto', target=dest).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        # In case of error (e.g., unsupported lang code), return original text
        return text

def detect_language(text):
    """
    Detects the language of the given text.
    """
    try:
        # deep-translator's detect method returns the language code
        lang = GoogleTranslator().detect(text)
        
        # The detect method might return a list, so we take the first element
        if isinstance(lang, list):
            lang = lang[0]
            
        return lang
    except Exception as e:
        print(f"Language detection error: {e}")
        # Default to English on error
        return "en"

