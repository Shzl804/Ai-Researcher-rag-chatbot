import re 

def remove_emails(text: str) -> str:
    email_patterns = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    return re.sub(email_patterns, " ", text)

def remove_urls(text: str) -> str:
    url_patterns = r"https?://\S+|www\.\S+"
    return re.sub(url_patterns, " ", text)

def remove_special_characters(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9\s.,!?():;'%+\-/]", " ", text)

def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text)

def clean_data(text: str) -> str:
    text = remove_emails(text)
    text = remove_special_characters(text)
    text = remove_urls(text)
    text = normalize_spaces(text)
    return text