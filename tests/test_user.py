from fastapi.testclient import TestClient

from .main import app
from .conftest import get_username, get_email, get_another_username, get_another_email, get_another_password


client = TestClient(app)


# Test User API
########################################################################


# Test user GET
def test_user_get_without_admin_token(get_user_token):
    response = client.get("/user", params={"token": get_user_token})
    assert response.status_code == 401
    print(response.text)


def test_user_get(get_admin_token):
    response = client.get("/user", params={"token": get_admin_token})
    assert response.status_code == 200
    print(response.text[0])


# Test user POST
def test_post_user(user_payload):
    response = client.post(f"/user/", params=user_payload)
    assert response.status_code == 201
    assert response.json()["username"] == get_username()
    assert response.json()["email"] == get_email()
    print(response.text)


def test_user_post_invalid_email(user_payload):
    response = client.post(f"/user/", params={**user_payload, "email": "wrongformat"})
    assert response.status_code == 422
    print(response.json()["detail"][0]["msg"])


def test_user_post_when_username_existed(user_payload):
    response = client.post(f"/user/", params={**user_payload, "email": "change@testmail.com"})
    assert response.status_code == 400
    print(response.text)


def test_user_post_when_email_existed(user_payload):
    response = client.post(f"/user/", params={**user_payload, "username": "ChangeUser"})
    assert response.status_code == 400
    print(response.text)
    

# Test user PATCH
def test_user_patch_which_username_do_not_exist(patch_user_payload):
    fake_username = "UserDoNotExist"
    response = client.patch(f"/user/{fake_username}", params={**patch_user_payload, "username": fake_username})
    assert response.status_code == 400
    print(response.text)


def test_user_patch_with_wrong_format_email(patch_user_payload):
    response = client.patch(f"/user/{get_username()}", params={**patch_user_payload, "email": "wrongformat"})
    assert response.status_code == 422
    print(response.json()["detail"][0]["msg"])


def test_user_patch_with_wrong_old_password(patch_user_payload):
    response = client.patch(f"/user/{get_username()}", params={**patch_user_payload, "old_password": "wrong_password"})
    assert response.status_code == 400
    print(response.json())


def test_user_patch_when_email_is_already_used_by_other_user(user_payload, patch_user_payload):
    response = client.post(f"/user/", params={**user_payload, "username": get_another_username(), "email": get_another_email()}) # create another user
    assert response.status_code == 201
    assert response.json()["username"] == get_another_username()
    assert response.json()["email"] == get_another_email()
    response = client.patch(f"/user/{get_username()}", params={**patch_user_payload, "email": get_another_email()})
    assert response.status_code == 400
    print(response.text)


def test_user_patch(patch_user_payload):
    response = client.patch(f"/user/{get_username()}", params={**patch_user_payload})
    assert response.status_code == 202
    print(response.text)


def test_login_after_user_patch_with_old_wrong_password(login_payload):
    response = client.post(f"/login", params=login_payload)
    response.status_code == 402
    print(response.text)


def test_login_after_user_patch_with_new_correct_password(login_payload):
    response = client.post(f"/login", params={**login_payload, "password": get_another_password()})
    response.status_code == 202
    print(response.text)

    
# Test user GET
def test_user_get_again(get_admin_token):
    response = client.get("/user", params={"token": get_admin_token})
    assert response.status_code == 200
    assert response.json()[0]["username"] != response.json()[1]["username"]
    assert response.json()[0]["email"] != response.json()[1]["email"]
    assert response.json()[2]["username"] != response.json()[1]["username"]
    print(response.json())
    

# Test user DELETE
def test_user_delete_when_user_do_not_exist(get_admin_token):
    fake_username = "dummy_user"
    response = client.delete(f"/user/{fake_username}", params={"username": fake_username, "token": get_admin_token})
    assert response.status_code == 404
    print(response.json())


def test_user_delete_without_admin_token(get_user_token):
    response = client.delete(f"/user/{get_username()}", params={"username": get_username(), "token": get_user_token})
    assert response.status_code == 401
    print(response.text)


def test_user_delete(get_admin_token):
    response = client.delete(f"/user/{get_username()}", params={"username": get_username(), "token": get_admin_token})
    assert response.status_code == 202
    assert response.json()["username"] == get_username()
    assert response.json()["email"] == get_email()
    print(response.text)

    response = client.delete(f"/user/{get_another_username()}", params={"username": get_another_username(), "token": get_admin_token})
    assert response.status_code == 202
    assert response.json()["username"] == get_another_username()
    assert response.json()["email"] == get_another_email()
    print(response.text)
