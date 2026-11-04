import pytest
import requests

from models.api_responses import APIMessage
from tests.api.test_catalog_api import BASE_URL
from utils.generate_user_data_for_api_tests import generate_user_data


@pytest.fixture(scope="session")
def api_session():
    """Создает единую сессию requests для всех API тестов (ускоряет прогон)"""
    session = requests.Session()

    yield session

    session.close()


@pytest.fixture
def create_delete_acc(api_session):
    user_obj, user_data = generate_user_data()

    create_response = api_session.post(f"{BASE_URL}/api/createAccount", data=user_data)

    assert create_response.status_code==200, f'Сервер вернул ошибку - {create_response.status_code}'
    validated_response = APIMessage(**create_response.json())
    assert validated_response.responseCode == 201, f'Ожидаемый responseCode - 201, получили {validated_response.responseCode}'
    assert "User created!" in validated_response.message, f"Ожидаемое сообщение - 'User created!', а получили - {validated_response.message}"

    yield user_obj, user_data

    delete_response = api_session.delete(f"{BASE_URL}/api/deleteAccount",
                                         data={"email": user_data["email"], "password": user_data["password"]})

    validated_response = APIMessage(**delete_response.json())
    assert validated_response.responseCode == 200, f'Ожидаемый responceCode - 201, получили {validated_response.responseCode}'
    assert "Account deleted!" in validated_response.message, f"Ожидаемое сообщение - 'Account deleted!', а получили - {validated_response.message}"
