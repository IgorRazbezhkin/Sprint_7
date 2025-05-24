import random
import string
import requests
from urls import endpoints


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_login():
    length = random.randint(2, 10)
    return generate_random_string(length)

def generate_password():
    return ''.join(random.choice(string.digits) for _ in range(4))

def create_courier(data):
    response = requests.post(endpoints['create_courier'], json=data)
    return response

def login_courier(login, password):
    response = requests.post(endpoints['login_courier'], json={"login": login, "password": password})
    return response

def get_courier_id_by_login(login, password):
    response = login_courier(login, password)
    if response.status_code == 200:
        return response.json().get("id")
    return None