import os
from configparser import ConfigParser

from dotenv import load_dotenv
from fastapi import status
from fastapi.testclient import TestClient

from app import app


if "AM_I_IN_A_DOCKER_CONTAINER" not in os.environ:
    load_dotenv()

# Reading necessary info from environment or config
user_name = os.environ["USER_NAME"]
password = os.environ["USER_PASSWORD"]


config = ConfigParser()
config.read("config/conf.conf")

client = TestClient(app=app)


def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "Hello World!"}


def test_sendfile():
    response = client.get("/sendfile")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/jpeg"


def test_secured_function_no_auth():
    response = client.get("/secured")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_secured_funtion_auth():
    response = client.get("/secured", auth=(user_name, password))
    assert response.status_code == status.HTTP_200_OK


def test_send_file_auth():
    sample_file = config["GENERAL"]["SAMPLE_FILE"]
    with open(sample_file, "rb") as file:
        file_content = file.read()
        content = {"file_to_process": (os.path.basename(file.name), file_content)}
    response = client.post("/postfile", files=content, auth=(user_name, password))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "file received"}


def test_send_file_no_auth():
    sample_file = config["GENERAL"]["SAMPLE_FILE"]
    with open(sample_file, "rb") as file:
        file_content = file.read()
        content = {"file_to_process": (os.path.basename(file.name), file_content)}
    response = client.post("/postfile", files=content)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
