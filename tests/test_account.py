from fastapi.testclient import TestClient

from .main import app
from .conftest import get_username, get_email, get_account, get_account_name, get_another_account_name, get_server, get_another_server


client = TestClient(app)


# Test Account API
############################################################################


# Test account GET
def test_account_get_when_no_account(get_admin_token):
    response = client.get("/account", params={"token": get_admin_token})
    assert response.status_code == 204


def test_account_get_when_no_account_without_admin_token(get_user_token):
    response = client.get("/account", params={"token": get_user_token})
    assert response.status_code == 401
    print(response.text)


# Test account POST
def test_post_account_when_user_do_not_exist(get_admin_token, account_payload):
    response = client.post("/account", params={"token": get_admin_token}, json=account_payload)
    print(response.json())
    assert response.status_code == 404


def test_post_account(user_payload, account_payload, login_payload):
    response = client.post("/user", params=user_payload)
    assert response.json()["username"] == get_username()
    assert response.json()["email"] == get_email()
    assert response.status_code == 201

    response = client.post("/login", params=login_payload)
    assert response.status_code == 202
    token = response.json()["access_token"]

    response = client.put(f"/user/{get_email()}", params={"email": get_email(), "token": token})
    assert response.status_code == 202
    assert response.json()["is_active"] == True
    

    response = client.post("/account", params={"token": token}, json=account_payload)
    assert response.json()["name"] == get_account_name()
    assert response.json()["account"] == get_account()
    assert response.json()["server"] == get_server()
    assert response.json()["owner_name"] == get_username()
    assert response.status_code == 201
    print(response.text)


def test_post_account_duplicated(login_payload, account_payload):
    response = client.post("/login", params=login_payload)
    assert response.status_code == 202
    token = response.json()["access_token"]

    response = client.post(f"/account", params={"token": token}, json=account_payload)
    assert response.status_code == 400
    print(response.text)
    

# Test account GET
def test_account_get(login_payload):
    response = client.post("/login", params=login_payload)
    assert response.status_code == 202
    token = response.json()["access_token"]

    response = client.get("/account", params={"token": token})
    assert response.json()[0]["name"] == get_account_name()
    assert response.json()[0]["account"] == get_account()
    assert response.json()[0]["server"] == get_server()
    assert response.json()[0]["owner_name"] == get_username()
    assert response.status_code == 200
    print(response.text)


# Test account PATCH
def test_patch_account(login_payload, account_payload_to_be_update):
    response = client.post("/login", params=login_payload)
    assert response.status_code == 202
    token = response.json()["access_token"]

    response = client.patch(f"/account/{get_account_name()}", params={"token": token}, json=account_payload_to_be_update)
    assert response.json()["name"] == get_another_account_name()
    assert response.json()["server"] == get_another_server()
    assert response.status_code == 202
    print(response.text)


def test_patch_account_when_account_do_not_exist(login_payload, account_payload_to_be_update):
    response = client.post("/login", params=login_payload)
    assert response.status_code == 202
    token = response.json()["access_token"]

    response = client.patch(f"/account/{get_account_name()}", params={"token": token}, json=account_payload_to_be_update)
    assert response.status_code == 404
    print(response.text)
    
    
# Test account DELETE
def test_delete_account(get_admin_token, account_payload_to_be_delete, login_payload):
    response = client.post("/login", params=login_payload)
    assert response.status_code == 202
    token = response.json()["access_token"]

    response = client.delete(f"/account/{get_another_account_name()}", params={**account_payload_to_be_delete, "token": token})
    assert response.json()["name"] == get_another_account_name()
    assert response.json()["server"] == get_another_server()
    assert response.status_code == 202
    
    response = client.delete(f"/user/{get_username()}", params={"username": get_username(), "token": get_admin_token})
    assert response.json()["username"] == get_username()
    assert response.json()["email"] == get_email()
    assert response.status_code == 202
    print(response.text)
    