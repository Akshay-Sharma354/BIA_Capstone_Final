import json
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'

_faq_cache = None
_products_cache = None
_policies_cache = None

def load_faq():
    global _faq_cache
    if _faq_cache is not None:
        return _faq_cache
    try:
        faq_path = DATA_DIR / 'FAQ.md'
        with open(faq_path, 'r', encoding='utf-8') as f:
            _faq_cache = f.read()
        return _faq_cache
    except Exception as e:
        return ""

def load_products():
    global _products_cache
    if _products_cache is not None:
        return _products_cache
    try:
        products_path = DATA_DIR / 'Products.json'
        with open(products_path, 'r', encoding='utf-8') as f:
            _products_cache = json.load(f)
        return _products_cache
    except Exception as e:
        return []

def load_policies():
    global _policies_cache
    if _policies_cache is not None:
        return _policies_cache
    try:
        policies_path = DATA_DIR / 'Policies.md'
        with open(policies_path, 'r', encoding='utf-8') as f:
            _policies_cache = f.read()
        return _policies_cache
    except Exception as e:
        return ""

def get_order_status(order_id: str) -> str:
    mock_orders = {
        "12345": "Order #12345 is SHIPPED. Expected delivery: May 30th",
        "67890": "Order #67890 is PROCESSING at our warehouse",
        "ABCDE": "Order #ABCDE has been DELIVERED"
    }
    return mock_orders.get(order_id, f"Order '{order_id}' not found")

def create_return_request(order_id: str, reason: str) -> str:
    return f"Return created for Order #{order_id}. Reason: {reason}. Process within 24 hours."

def get_answer(query: str) -> str:
    try:
        from google import genai
        
        faq = load_faq()
        policies = load_policies()
        products = json.dumps(load_products(), indent=2)
        
        system_prompt = f"""You are a professional E-Commerce Customer Support AI Agent.

KNOWLEDGE BASE:
--- FAQ ---
{faq}

--- POLICIES ---
{policies}

--- PRODUCTS ---
{products}

Guidelines:
1. Answer using the knowledge base above
2. Be polite and professional
3. Never make up information
"""
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "API key not configured."
        
        client = genai.Client(api_key=api_key)
        
        full_prompt = system_prompt + "\n\nUser: " + query
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "Unable to generate response. Please try again."
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return f"Error occurred. Please contact support@example.com"
