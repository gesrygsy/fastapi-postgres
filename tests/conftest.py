import random
import pytest


# Before run pytest, you must CREATE an admin account on admin side, COPY & PASTE 'token' to below 'get_admin_token' function after verified email account.
@pytest.fixture
def get_admin_token() -> str:
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGlybyIsImV4cCI6MTcwNTk5ODIzM30.WK5herUN8-66-tod5rnleAUj8qi2m-1JP70zBCzYJHg"


# 'get_user_token' is just a mock token string for testing, make sure the 'get_admin_token' is correct.
@pytest.fixture
def get_user_token() -> str:
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJOZXdVc2VyIiwiZXhwIjoxNzA1ODI0OTQzfQ.LpST12C9WrFh63hlH0OtjPWSRbDsJmMckTDo9Kvr1JY"


def get_function_name() -> str:
    return "FunctionTest"


@pytest.fixture
def dataset_payload() -> dict:
    return {
        "function": get_function_name(),
        "type": "Currency",
        "description": "test description",
        "data_source": "test data_source"
    }


def get_symbol_name() -> str:
    return "TESTSYMBOL"


def get_datetime() -> str:
    return "2024-01-01 00:00:00.0"


@pytest.fixture
def currency_payload() -> dict:
    return {
        "function": get_function_name(),
        "type": "Currency",
        "symbol": get_symbol_name(),
        "datetime": get_datetime(),
        "open": random.random(),
        "high": random.random(),
        "low": random.random(),
        "close": random.random(),
        "volume": None
    }


@pytest.fixture
def currency_params() -> dict:
    return {
        "function": get_function_name(),
        "type": "Currency"
    }


@pytest.fixture
def symbol_params() -> dict:
    return {
        "function": get_function_name(),
        "symbol": get_symbol_name()
    }


@pytest.fixture
def symbol_params_for_delete() -> dict:
    return {
        "function": get_function_name(),
        "symbol": get_symbol_name()
    }


def get_username() -> str:
    return "TestUser"


def get_email() -> str:
    return "test@testmail.com"


def get_password() -> str:
    return "password"


def get_another_email() -> str:
    return "another@testmail.com"


def get_another_username() -> str:
    return "AnotherUser"


def get_another_password() -> str:
    return "drowssap"


@pytest.fixture
def user_payload() -> dict:
    return {
        "username": get_username(),
        "email": get_email(),
        "password": get_password(),
        # "role": 2,
    }


@pytest.fixture
def patch_user_payload() -> dict:
    return {
        "username": get_username(),
        "email": get_email(),
        "old_password": get_password(),
        "new_password": get_another_password(),
    }


def get_account_name() -> str:
    return "DummyAccount"


def get_account() -> str:
    return "12345"


def get_server() -> str:
    return "ServerStub"


def get_another_server() -> str:
    return "FakeServer"


def get_another_account_name() -> str:
    return "MockAccount"


@pytest.fixture
def account_payload() -> dict:
    return {
        "name": get_account_name(),
        "account": get_account(),
        "password": get_password(),
        "server": get_server(),
        "owner_name": get_username()
    }


@pytest.fixture
def account_payload_to_be_update() -> dict:
    return {
        "name": get_account_name(),
        "account": get_account(),
        "server": get_server(),
        "owner_name": get_username(),
        "new_name": get_another_account_name(),
        "new_account": get_account(),
        "new_server": get_another_server(),
        "new_password": "54321"
    }


@pytest.fixture
def account_payload_to_be_delete() -> dict:
    return {
        "name": get_another_account_name(),
        "account": get_account(),
        "server": get_another_server(),
        "owner_name": get_username()
    }


@pytest.fixture
def login_payload() -> dict:
    return {
        "username": get_username(),
        "password": get_password(),
    }
