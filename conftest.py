import pytest
import requests
from helpers import generate_login, generate_password
from data import courier_first_name
from urls import endpoints


@pytest.fixture
def courier_data():
    login = generate_login()
    password = generate_password()
    data = {
        "login": login,
        "password": password,
        "firstName": courier_first_name
    }
    return data

@pytest.fixture
def created_courier_with_id(courier_data):
    response = requests.post(endpoints['create_courier'], json=courier_data)
    assert response.status_code == 201

    login_response = requests.post(endpoints['login_courier'], json={
        "login": courier_data["login"],
        "password": courier_data["password"]
    })
    login_response.raise_for_status()
    courier_id = login_response.json().get("id")
    assert courier_id is not None

    yield {**courier_data, "id": courier_id}

    delete_response = requests.delete(endpoints['delete_courier'].replace("{id}", str(courier_id)))
    assert delete_response.status_code in [200, 404]

@pytest.fixture
def create_order_and_get_id():
    order_data = {
        "firstName": "Павел",
        "lastName": "Смородинов",
        "address": "Чернышевского д.82, кв. 6",
        "metroStation": 4,
        "phone": "+8 987 654 32 10",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "",
        "color": ["BLACK"]
    }
    response = requests.post(endpoints['create_order'], json=order_data)
    response.raise_for_status()
    track = response.json().get('track')
    assert track is not None

    response_track = requests.get(endpoints['track_order'], params={"t": track})
    response_track.raise_for_status()
    order_info = response_track.json()
    order_id = order_info['order']['id']
    assert order_id is not None

    yield {
        'track': track,
        'order_id': order_id
    }