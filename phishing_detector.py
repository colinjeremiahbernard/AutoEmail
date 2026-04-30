import re
import tldextract

SUSPICIOUS_KEYWORDS = [
    "urgent", "verify your account", "password", "click here",
    "bank", "login", "suspended"
]

def contains_suspicious_links(text):
    urls = re.findall(r'https?://\S+', text)
    for url in urls:
        domain = tldextract.extract(url).domain
        if domain not in ["google", "microsoft", "amazon"]:
            return True
    return False

def is_phishing(email_text):
    text_lower = email_text.lower()

    keyword_flag = any(word in text_lower for word in SUSPICIOUS_KEYWORDS)
    link_flag = contains_suspicious_links(email_text)

    return keyword_flag or link_flag