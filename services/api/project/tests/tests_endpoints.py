import os

import jwt
import requests
from dotenv import dotenv_values
from faker import Faker
from flask import json

from project.utils.const import PWD_CONTEXT

config = dotenv_values(f'{os.getenv("PROJECT_GALLERY")}.env')

fake = Faker()
header = {"Accept": "*/*","content-type": "application/json"}

def tests_alive():
    resp = requests.get("http://127.0.0.1:5000/api/alive")
    data = resp.json()
    assert resp.status_code == 200
    assert "alive" in data["message"]
    assert "success" in data["status"]


def tests_create_user():
    data = {"password": fake.password(8), "email": fake.email(), "name": fake.name()}
    resp = requests.post(
        "http://127.0.0.1:5000/api/users", headers=header, data=json.dumps(data)
    )
    assert resp.status_code == 200
    assert PWD_CONTEXT.verify(data["password"], resp.json()["password"])


def test_login_user():
    data_create = {"password": fake.password(8), "email": fake.email(), "name": fake.name()}
    resp = requests.post(
        "http://127.0.0.1:5000/api/users", headers=header, data=json.dumps(data_create)
    )
    assert resp.status_code == 200
    
    data_login = {"password": data_create['password'], "email": data_create["email"]}
    resp = requests.post(
        "http://127.0.0.1:5000/api/login", headers=header, data=json.dumps(data_login)
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert "refresh_token" in resp.json()
    

def test_create_album():
    data_create = {"password": fake.password(8), "email": fake.email(), "name": fake.name()}
    resp = requests.post(
        "http://127.0.0.1:5000/api/users", headers=header, data=json.dumps(data_create)
    )
    assert resp.status_code == 200
    
    data_login = {"password": data_create['password'], "email": data_create["email"]}
    resp = requests.post(
        "http://127.0.0.1:5000/api/login", headers=header, data=json.dumps(data_login)
    )
    assert resp.status_code == 200
    
    assert "access_token" in resp.json()
    assert "refresh_token" in resp.json()
    
    decode = jwt.decode(resp.json()['access_token'], config['SECRET_KEY'], algorithms=['HS256', ])
    assert decode['sub']['email'] == data_login['email']
    
    data = {"name": fake.name()}
    resp = requests.post(
        "http://127.0.0.1:5000/api/albums", headers=header, data=json.dumps(data)
    )

    
    