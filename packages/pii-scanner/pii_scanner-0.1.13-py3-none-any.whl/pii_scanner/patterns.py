import re

# Regex patterns for PII detection
PII_PATTERNS = {
    'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'phone': r'\+?\d[\d -]{8,12}\d',
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    'credit_card': r'\b(?:\d[ -]*?){13,16}\b',
    'name': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Simple pattern for names
    'address': r'\d{1,5} [A-Za-z ]+, [A-Za-z ]+, [A-Z]{2} \d{5}'
}
