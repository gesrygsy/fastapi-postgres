from fastapi.testclient import TestClient

from .main import app
from .conftest import get_function_name


client = TestClient(app)


# Test Dataset API
##################################################################


# Test dataset GET
def test_get_dataset_without_admin_token(get_user_token):
    response = client.get("/dataset", params={"token": get_user_token})
    assert response.status_code == 401
    print(response.text)


def test_get_dataset_with_wrong_format_token():
    response = client.get("/dataset", params={"token": "FAKE_TOKEN"})
    assert response.status_code == 401
    print(response.text)


def test_get_dataset_when_data_do_not_exist(get_admin_token):
    response = client.get("/dataset", params={"token": get_admin_token})
    assert response.status_code == 204
    print(response.text)
    

# Test dataset function POST
def test_post_dataset_without_admin_token(get_user_token, dataset_payload):
    response = client.post("/dataset", params={**dataset_payload, "token": get_user_token})
    assert response.status_code == 401
    print(response.text)


def test_post_dataset_with_wrong_format_token(dataset_payload):
    response = client.post("/dataset", params={**dataset_payload, "token": "FAKE_TOKEN"})
    assert response.status_code == 401
    print(response.text)


def test_post_dataset(get_admin_token, dataset_payload):
    response = client.post("/dataset", params={**dataset_payload, "token": get_admin_token})
    assert response.json()["function"] == get_function_name()
    assert response.status_code == 201
    print(response.text)


def test_post_dataset_when_function_already_existed(get_admin_token, dataset_payload):
    response = client.post("/dataset", params={**dataset_payload, "token": get_admin_token})
    assert response.status_code == 400
    print(response.text)


# Test dataset GET
def test_get_dataset_when_data_exist_without_admin_token(get_user_token):
    response = client.get("/dataset", params={"token": get_user_token})
    assert response.status_code == 401
    print(response.text)


def test_get_dataset_when_data_exist(get_admin_token):
    response = client.get("/dataset", params={"token": get_admin_token})
    assert response.json()[0]["function"] == get_function_name()
    assert response.status_code == 200
    print(response.text)


# Test dataset function GET
def test_get_dataset_function_when_data_exist_without_admin_token(get_user_token):
    response = client.get(f"/dataset/{get_function_name()}", params={"token": get_user_token})
    assert response.status_code == 401
    print(response.text)


def test_get_dataset_function_when_data_exist(get_admin_token):
    response = client.get(f"/dataset/{get_function_name()}", params={"token": get_admin_token})
    assert response.json()["function"] == get_function_name()
    assert response.status_code == 200
    print(response.text)


# Test dataset function PATCH
def test_patch_dataset_function_when_data_do_not_exist_without_admin_token(get_user_token, dataset_payload):
    response = client.patch(f"/dataset/FakeFunction", params={**dataset_payload, "data_source": "update", "token": get_user_token})
    assert response.status_code == 401
    print(response.text)


def test_patch_dataset_function_when_data_do_not_exist(get_admin_token, dataset_payload):
    response = client.patch(f"/dataset/FakeFunction", params={**dataset_payload, "data_source": "update", "token": get_admin_token})
    assert response.status_code == 404
    print(response.text)


def test_patch_dataset_function_when_data_exist_without_admin_token(get_user_token, dataset_payload):
    response = client.patch(f"/dataset/{get_function_name()}", params={**dataset_payload, "data_source": "update", "token": get_user_token})
    assert response.status_code == 401
    print(response.text)


def test_patch_dataset_function_when_data_exist(get_admin_token, dataset_payload):
    response = client.patch(f"/dataset/{get_function_name()}", params={**dataset_payload, "data_source": "update", "token": get_admin_token})
    assert response.json()["data_source"] == "update"
    assert response.status_code == 202
    print(response.text)


# Test dataset function DELETE
def test_delete_dataset_without_admin_token(get_user_token):
    response = client.delete(f"/dataset/{get_function_name()}", params={"token": get_user_token})
    assert response.status_code == 401
    print(response.text)


def test_delete_dataset(get_admin_token):
    response = client.delete(f"/dataset/{get_function_name()}", params={"token": get_admin_token})
    assert response.json()["function"] == get_function_name()
    assert response.status_code == 202
    print(response.text)

# Test dataset function DELETE when symbol data existed is the part of the Test Currency API
