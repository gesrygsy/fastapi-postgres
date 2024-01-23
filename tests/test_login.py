# to be test
from fastapi.testclient import TestClient

from .main import app
from .conftest import get_username, get_email, get_admin_token


client = TestClient(app)


# Test login API
########################################################################

# Test login POST
def test_login_post_when_user_do_not_exist(login_payload):
    response = client.post(f"/login", params=login_payload)
    assert response.status_code == 400
    print(response.text)


def test_login_post_with_wrong_password(user_payload, login_payload):
    response = client.post(f"/user/", params=user_payload)
    assert response.status_code == 201
    assert response.json()["username"] == get_username()
    assert response.json()["email"] == get_email()

    response = client.post(f"/login", params={**login_payload, "password": "wrong_password"})
    assert response.status_code == 400
    print(response.text)


def test_login_post_and_check_verify(get_admin_token, login_payload):
    response = client.post(f"/login", params=login_payload)
    assert response.status_code == 202
    print(f"{response.json()['description']}")

    response = client.get(f"/user", params={"token": get_admin_token})
    assert response.status_code == 200
    for r in response.json():
        if r["username"] == get_username():
            assert r["is_active"] == False
            print(r)


def test_login_post_and_verify_email(login_payload):
    response = client.post(f"/login", params=login_payload)
    assert response.status_code == 202
    token = response.json()['access_token']

    response = client.put(f"/user/{get_email()}", params={"email": get_email(), "token": token})
    assert response.status_code == 202
    assert response.json()["is_active"] == True
    print(response.text)


# Test login DELETE
def test_login_delete_user_when_username_do_not_exist(get_admin_token):
    fake_username = "FakeUser"
    response = client.delete(f"/user/{fake_username}", params={"username": fake_username, "token": get_admin_token})
    assert response.status_code == 404
    print(response.text)


def test_login_delete_user_without_admin_token(get_user_token):
    response = client.delete(f"/user/{get_username()}", params={"username": get_username(), "token": get_user_token})
    assert response.status_code == 401
    print(response.text)


def test_login_delete_user(get_admin_token):
    response = client.delete(f"/user/{get_username()}", params={"username": get_username(), "token": get_admin_token})
    assert response.status_code == 202
    assert response.json()["username"] == get_username()
    assert response.json()["email"] == get_email()
    print(response.text)