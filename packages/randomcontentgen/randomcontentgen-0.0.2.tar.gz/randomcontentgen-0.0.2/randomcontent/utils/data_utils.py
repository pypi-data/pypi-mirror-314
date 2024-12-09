# randomcontent/utils/data_utils.py

import random

def generate_name():
    first_names = ["Alice", "Bob", "Charlie", "Diana"]
    last_names = ["Smith", "Johnson", "Williams", "Brown"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_email():
    domains = ["example.com", "test.com", "demo.org"]
    return f"{generate_name().replace(' ', '.').lower()}@{random.choice(domains)}"
