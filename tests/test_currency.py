from fastapi.testclient import TestClient

from .main import app
from .conftest import get_username, get_email, get_function_name, get_symbol_name, get_datetime


client = TestClient(app)


# Test Currency API
############################################################################
def get_current_user_token(login_payload):
    response = client.post("/login", params=login_payload)
    assert response.status_code == 202
    return response.json()["access_token"]

    
# Test currency GET all
def test_currency_get_with_wrong_token(get_user_token):
    response = client.get("/currency", params={"token": get_user_token})
    assert response.status_code == 401
    print(response.text)


def test_get_currency_with_user_did_not_verify(login_payload, user_payload):
    response = client.post("/user", params=user_payload)
    assert response.status_code == 201
    assert response.json()["username"] == get_username()
    assert response.json()["email"] == get_email()

    token = get_current_user_token(login_payload)

    response = client.get("/currency", params={"token": token})
    assert response.status_code == 400
    print(response.text)


def test_get_currency_when_data_do_not_exist(login_payload):
    token = get_current_user_token(login_payload)

    response = client.put(f"/user/{get_email()}", params={"email": get_email(), "token": token})
    assert response.status_code == 202
    assert response.json()["is_active"] == True

    response = client.get("/currency", params={"token": token})
    assert response.status_code == 204
    print(response.text)


# Test currency POST
def test_post_currency_when_dataset_do_not_exist(get_admin_token, currency_params, currency_payload):
    response = client.post(f"/currency/{get_function_name()}", params={**currency_params, "token": get_admin_token}, json=currency_payload)
    assert response.status_code == 404
    print(response.text)


def test_post_currency(get_admin_token, dataset_payload, currency_params, currency_payload):
    response = client.post("/dataset", params={**dataset_payload, "token": get_admin_token})
    assert response.status_code == 201
    assert response.json()["function"] == get_function_name()

    response = client.post(f"/currency/{get_function_name()}", params={**currency_params, "token": get_admin_token}, json=currency_payload)
    assert response.status_code == 201
    assert response.json()["symbol"] == get_symbol_name()
    print(response.text)


def test_post_currency_without_admin_token(currency_params, currency_payload, login_payload):
    token = get_current_user_token(login_payload)

    response = client.post(f"/currency/{get_function_name()}", params={**currency_params, "token": token}, json={**currency_payload, "symbol": "OTHER"})
    assert response.status_code == 400
    print(response.text)


def test_post_currency_when_data_already_existed(get_admin_token, currency_params, currency_payload):
    response = client.post(f"/currency/{get_function_name()}", params={**currency_params, "token": get_admin_token}, json=currency_payload)
    assert response.status_code == 400
    print(response.text)

    
# Test currency GET all
def test_get_currency(login_payload):
    token = get_current_user_token(login_payload)

    response = client.get("/currency", params={"token": token})
    assert response.status_code == 200
    assert response.json()[0]["symbol"] == get_symbol_name()
    print(response.text)

    
# Test currency GET symbol
def test_get_symbol(symbol_params, login_payload):
    token = get_current_user_token(login_payload)

    response = client.get(f"/currency/{get_function_name()}/{get_symbol_name()}", params={**symbol_params, "token": token})
    assert response.status_code == 200
    assert response.json()[0]["symbol"] == get_symbol_name()
    print(response.text)


def test_get_symbol_when_symbol_data_do_not_exist(symbol_params, login_payload):
    token = get_current_user_token(login_payload)

    response = client.get(f"/currency/{get_function_name()}/NEXIST", params={**symbol_params, "symbol": "NEXIST", "token": token})
    assert response.status_code == 404
    print(response.text)


# Test Dataset DELETE when symbol data existed
def test_delete_dataset_when_symbol_data_existed(get_admin_token):
    response = client.delete(f"/dataset/{get_function_name()}", params={"token": get_admin_token})
    assert response.status_code == 400
    print(response.text)


# Test currency DELETE symbol specific data
def test_delete_currency_symbol_specific_data_do_not_exist(get_admin_token, symbol_params_for_delete):
    response = client.delete(f"/currency/{get_function_name()}/{get_symbol_name()}/2024-01-02 00:00:00.0", params={**symbol_params_for_delete, "datetime": "2024-01-02 00:00:00.0", "token": get_admin_token})
    assert response.status_code == 404
    print(response.text)


def test_delete_currency_symbol_specific_data_without_admin_token(login_payload, symbol_params_for_delete):
    token = get_current_user_token(login_payload)

    response = client.delete(f"/currency/{get_function_name()}/{get_symbol_name()}/{get_datetime()}", params={**symbol_params_for_delete, "datetime": get_datetime(), "token": token})
    assert response.status_code == 400
    print(response.text)


def test_delete_currency_symbol_specific_data(get_admin_token, symbol_params_for_delete):
    response = client.delete(f"/currency/{get_function_name()}/{get_symbol_name()}/{get_datetime()}", params={**symbol_params_for_delete, "datetime": get_datetime(), "token": get_admin_token})
    assert response.json()["symbol"] == get_symbol_name()
    assert response.status_code == 202
    print(response.text)


# Test currency DELETE symbol all data
def test_delete_when_symbol_data_do_not_exist(get_admin_token, currency_params, currency_payload, symbol_params_for_delete):
    response = client.post(f"/currency/{get_function_name()}", params={**currency_params, "token": get_admin_token}, json=currency_payload)
    assert response.status_code == 201
    assert response.json()["symbol"] == get_symbol_name()

    response = client.delete(f"/currency/{get_function_name()}/NEXIST", params={**symbol_params_for_delete, "symbol": "NEXIST", "token": get_admin_token})
    assert response.status_code == 404
    print(response.text)


def test_delete_symbol_data(get_admin_token, symbol_params_for_delete):
    response = client.delete(f"/currency/{get_function_name()}/{get_symbol_name()}", params={**symbol_params_for_delete, "token": get_admin_token})
    assert response.json()[0]["symbol"] == get_symbol_name()
    assert response.status_code == 202

    # Delete and clean Dataset before complete
    response = client.delete(f"/dataset/{get_function_name()}", params={"token": get_admin_token})
    assert response.json()["function"] == get_function_name()
    assert response.status_code == 202

    # Delete and clean User data
    response = client.delete(f"/user/{get_username()}", params={"username": get_username(), "token": get_admin_token})
    assert response.json()["username"] == get_username()
    assert response.json()["email"] == get_email()
    assert response.status_code == 202
    print(response.text)