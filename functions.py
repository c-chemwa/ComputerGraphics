import re

def generate_email(name):
    parts = re.findall(r'\w+', name.lower())
    if len(parts) >= 2:
        email = f"{parts[0][0]}{parts[-1]}@gmail.com"
    else:
        email = f"{parts[0]}@gmail.com"
    return email

def has_special_chars(name):
    return bool(re.search(r'[^a-zA-Z\s]', name))