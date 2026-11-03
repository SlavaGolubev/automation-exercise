import random
import allure
import pytest
from pydantic import ValidationError
from models.api_responses import APIError, ProductsResponse, BrandsResponse, APIMessage, UserDetailsResponse
from models.user import RegistrationData
from utils.generate_user_data_for_api_tests import generate_user_data

BASE_URL = "https://automationexercise.com"


@allure.epic('API Testing')
@allure.feature('Catalog API')
@allure.story('Successful GET requests')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("path, response_model", [
    ('/api/productsList', ProductsResponse),
    ('/api/brandsList', BrandsResponse)
], ids=['GET products', 'GET brands'])
def test_get_catalog_endpoints_success(api_session, path, response_model):
    """Тестируем успешные GET запросы к спискам продуктов и брендов"""

    with allure.step(f"Отправляем GET запрос к {path}"):
        response = api_session.get(f"{BASE_URL}{path}")

    with allure.step("Проверяем HTTP статус-код"):
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

    with allure.step("Валидируем структуру ответа через Pydantic"):
        response_data = response.json()
        try:
            validated_response = response_model(**response_data)

            if hasattr(validated_response, 'products'):
                assert len(validated_response.products) > 0, "Список продуктов пустой"
            elif hasattr(validated_response, 'brands'):
                assert len(validated_response.brands) > 0, "Список брендов пустой"

        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации структуры ответа {path}:\n{e}")

    with allure.step("Прикрепляем валидированный JSON в отчет"):
        allure.attach(
            validated_response.model_dump_json(indent=2),
            name=f"Validated {path} response",
            attachment_type=allure.attachment_type.JSON
        )


@allure.epic('API Testing')
@allure.feature('Catalog API')
@allure.story('Invalid HTTP methods')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("path, method", [
    ('/api/productsList', 'POST'),
    ('/api/productsList', 'PUT'),
    ('/api/brandsList', 'POST'),
    ('/api/brandsList', 'PUT')
], ids=['POST products', 'PUT products', 'POST brands', 'PUT brands'])
def test_catalog_endpoints_invalid_method(api_session, path, method):
    """Тестируем, что неподдерживаемые методы возвращают корректную ошибку"""

    with allure.step(f"Отправляем {method} запрос к {path}"):
        response = api_session.request(method, f"{BASE_URL}{path}")

    with allure.step("Проверяем, что HTTP статус все равно 200 (особенность этого API)"):
        assert response.status_code == 200

    with allure.step("Валидируем структуру ошибки через Pydantic"):
        response_data = response.json()
        try:
            validated_error = APIError(**response_data)
            assert validated_error.responseCode == 405, \
                f"Ожидался responseCode 405, получен {validated_error.responseCode}"
            assert "not supported" in validated_error.message.lower(), \
                f"Неожиданное сообщение об ошибке: {validated_error.message}"
        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации ответа об ошибке {path}:\n{e}")

    with allure.step("Прикрепляем валидированный JSON ошибки в отчет"):
        allure.attach(
            validated_error.model_dump_json(indent=2),
            name=f"Validated {method} {path} error response",
            attachment_type=allure.attachment_type.JSON
        )


@allure.epic('API Testing')
@allure.feature('Search product')
@allure.story('Successful POST request')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("query, expected_has_results", [
    ("top", True),
    ("shoes", False)
], ids=["search=top (success)", "search=shoes (no result)"])
def test_search_products_success(api_session, query, expected_has_results):
    """Тестируем POST запрос для поиска продукта"""

    with allure.step(f"Отправляем POST запрос к /api/searchProduct с запросом '{query}'"):
        response = api_session.post(f"{BASE_URL}/api/searchProduct", data={"search_product": query})

    with allure.step("Проверяем, что HTTP статус равен 200"):
        assert response.status_code == 200, f"Ожидался HTTP 200, получен {response.status_code}"

    with allure.step("Валидируем структуру ответа через Pydantic"):
        response_data = response.json()
        try:
            validated_response = ProductsResponse(**response_data)

            assert validated_response.responseCode == 200, \
                f"Ожидался responseCode 200, фактический: {validated_response.responseCode}"

            actual_has_results = bool(validated_response.products)

            assert actual_has_results == expected_has_results, \
                f"При поиске '{query}' ожидалось наличие результатов={expected_has_results}, " \
                f"фактически найдено товаров: {len(validated_response.products)}"

        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации структуры ответа:\n{e}")

    with allure.step("Прикрепляем валидированный JSON в отчет"):
        allure.attach(
            validated_response.model_dump_json(indent=2, ensure_ascii=False),
            name=f"Validated search response for '{query}'",
            attachment_type=allure.attachment_type.JSON
        )


@allure.epic('API Testing')
@allure.feature('Search product')
@allure.story('Invalid POST request (missing parameter)')
@allure.severity(allure.severity_level.CRITICAL)
def test_search_products_invalid_missing_param(api_session):
    """Тестируем POST запрос к поиску с пустым телом (отсутствует обязательный параметр)"""

    with allure.step("Отправляем POST запрос к /api/searchProduct с пустым телом"):
        response = api_session.post(f"{BASE_URL}/api/searchProduct", data={})

    with allure.step("Проверяем, что HTTP статус все равно 200 (особенность этого API)"):
        assert response.status_code == 200

    with allure.step("Валидируем структуру ответа об ошибке через Pydantic"):
        response_data = response.json()
        try:
            validated_response = APIError(**response_data)

            assert validated_response.responseCode == 400, \
                f"Ожидался responseCode 400, фактический: {validated_response.responseCode}"

            assert "parameter is missing in POST request" in validated_response.message, \
                f"Неожиданное сообщение об ошибке: {validated_response.message}"

        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации структуры ответа об ошибке:\n{e}")

    with allure.step("Прикрепляем валидированный JSON ошибки в отчет"):
        allure.attach(
            validated_response.model_dump_json(indent=2, ensure_ascii=False),
            name="Validated API Error response",
            attachment_type=allure.attachment_type.JSON
        )


@allure.epic('API Testing')
@allure.feature('Delete user endpoint')
@allure.story('Valid CREATE/DELETE user request')
@allure.severity(allure.severity_level.CRITICAL)
def test_create_delete_user(api_session):
    """Тестируем создание/удаление(CREATE/DELETE) аккаунта"""

    with allure.step("Сгенерируем данные для регистрации пользователя, которого будем удалять."):
        user_obj, user_data = generate_user_data()

    with allure.step("Отправляем POST запрос для регистрации пользователя."):
        response = api_session.post(f"{BASE_URL}/api/createAccount", data=user_data)

    with allure.step("Проверяем, что HTTP статус все равно 200 (особенность этого API)"):
        assert response.status_code == 200

    with allure.step("Валидируем структуру ответа запроса create_user через Pydantic"):
        try:
            validated_response = APIMessage(**response.json())
            assert validated_response.responseCode == 201, f'Ожидаемый responseCode - 201, получили {validated_response.responseCode}'
            assert "User created!" in validated_response.message, f"Ожидаемое сообщение - 'User created!', а получили - {validated_response.message}"

        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации структуры ответа об ошибке:\n{e}")

        allure.attach(validated_response.model_dump_json(indent=2, ensure_ascii=False),
                      attachment_type=allure.attachment_type.JSON,
                      name="Validated 'create user' API response ")

    with allure.step("Отправляем DELETE запрос для удаления аккаунта с email и password в теле запроса."):
        response = api_session.delete(f"{BASE_URL}/api/deleteAccount",
                                      data={"email": user_data["email"], "password": user_data["password"]})

    with allure.step("Проверяем, что HTTP статус 200"):
        assert response.status_code == 200

    with allure.step("Валидируем структуру ответа запроса delete_user через Pydantic"):
        try:
            validated_response = APIMessage(**response.json())
            assert validated_response.responseCode == 200, f'Ожидаемый responseCode - 201, получили {validated_response.responseCode}'
            assert "Account deleted!" in validated_response.message, f"Ожидаемое сообщение - 'Account deleted!', а получили - {validated_response.message}"

        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации структуры ответа об ошибке:\n{e}")

        allure.attach(validated_response.model_dump_json(indent=2, ensure_ascii=False),
                      attachment_type=allure.attachment_type.JSON,
                      name="Validated 'delete user' API response ")


@allure.epic('API Testing')
@allure.feature('Update user endpoint')
@allure.story('PUT request to update user data')
@allure.severity(allure.severity_level.CRITICAL)
def test_update_user(api_session, create_delete_acc):
    """Тестируем изменение(PUT) данных аккаунта и проверяем, что они действительно обновились"""

    user_obj, user_data = create_delete_acc

    field_for_update = random.choice([
        "birth_day", "birth_month", "birth_year",
        "company", "address1", "address2", "country",
        "city", "state", "zipcode", "mobile_number"
    ])

    with allure.step("Получаем исходные данные пользователя через getUserDetailByEmail"):
        initial_response = api_session.get(
            f"{BASE_URL}/api/getUserDetailByEmail?email={user_obj.email}",
        )
        assert initial_response.status_code == 200
        initial_data = UserDetailsResponse(**initial_response.json())
        initial_field_value = getattr(initial_data.user, field_for_update)

    new_user_data = RegistrationData.generate_data()
    new_field_value = getattr(new_user_data, field_for_update)

    with allure.step(f"Отправляем PUT запрос для изменения поля '{field_for_update}'"):
        response = api_session.put(
            f"{BASE_URL}/api/updateAccount",
            data={
                "email": user_obj.email,
                "password": user_obj.password,
                field_for_update: new_field_value
            }
        )

    with allure.step("Проверяем HTTP статус 200"):
        assert response.status_code == 200

    with allure.step("Валидируем структуру ответа"):
        validated_response = APIMessage(**response.json())
        assert validated_response.responseCode == 200
        assert "User updated!" in validated_response.message

    with allure.step("Проверяем, что поле действительно обновилось в системе"):
        updated_response = api_session.get(
            f"{BASE_URL}/api/getUserDetailByEmail",
            params={"email": user_obj.email, "password": user_obj.password}
        )
        assert updated_response.status_code == 200
        updated_data = UserDetailsResponse(**updated_response.json())
        updated_field_value = getattr(updated_data.user, field_for_update)

        assert updated_field_value != initial_field_value, \
            f"Поле '{field_for_update}' не обновилось. Было: {initial_field_value}, стало: {updated_field_value}"

        assert updated_field_value == new_field_value, \
            f"Поле '{field_for_update}' не совпадает с ожидаемым. Ожидалось: {new_field_value}, получено: {updated_field_value}"

    with allure.step("Прикрепляем валидированный JSON в отчет"):
        allure.attach(
            validated_response.model_dump_json(indent=2, ensure_ascii=False),
            name="Validated 'update user' API response",
            attachment_type=allure.attachment_type.JSON
        )


@allure.epic('API Testing')
@allure.feature('Get user account detail endpoint')
@allure.story('GET request to get user account detail by email')
@allure.severity(allure.severity_level.CRITICAL)
def test_get_user_data(api_session, create_delete_acc):
    user_obj, user_data = create_delete_acc

    with allure.step("Отправляем GET запрос на эндпоинт аккаунта"):
        response = api_session.get(f"{BASE_URL}/api/getUserDetailByEmail?email={user_obj.email}")

    with allure.step("Проверяем, что HTTP статус 200"):
        assert response.status_code == 200

    with allure.step("Валидируем структуру ответа запроса к данным аккаунта через Pydantic"):
        try:
            validated_response = UserDetailsResponse(**response.json())
            assert validated_response.responseCode == 200, f'Ожидаемый responseCode - 200, получили {validated_response.responseCode}'
            assert validated_response.user.email == user_obj.email
            assert validated_response.user.first_name == user_obj.first_name

        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации структуры ответа об ошибке:\n{e}")

        allure.attach(validated_response.model_dump_json(indent=2, ensure_ascii=False),
                      attachment_type=allure.attachment_type.JSON,
                      name="Validated 'update user' API response ")


@allure.epic('API Testing')
@allure.feature('Verify login endpoint')
@allure.story('Valid POST request')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("email, password, expected_response_code, expected_message",
                         [
                             ("tyubik@mail.com", "7582450", 200, "User exists!"),
                             ("tyubik@gmail.com", "743390", 404, "User not found!")
                         ],
                         ids=["registered_user", "unregistered_user"]
                         )
def test_login_verify_valid(api_session, email, password, expected_response_code, expected_message):
    """Тестируем POST запрос для авторизации пользователя по email и password"""

    with allure.step("Отправляем POST запрос для авторизации пользователя с email и password  в теле запроса."):
        response = api_session.post(f"{BASE_URL}/api/verifyLogin", data={"email": email, "password": password})

    with allure.step("Проверяем, что HTTP статус равен 200"):
        assert response.status_code == 200, f"Ожидался HTTP 200, получен {response.status_code}"

    with allure.step("Валидируем структуру ответа через Pydantic"):
        response_data = response.json()
        try:
            validated_response = APIMessage(**response_data)

            assert expected_response_code == validated_response.responseCode, f'Ожидаемый responseCode - {expected_response_code}, получили {validated_response.responseCode}'
            assert expected_message == validated_response.message, f"Ожидаемое сообщение - {expected_message}, а получили - {validated_response.message}"

        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации структуры ответа об ошибке:\n{e}")

        allure.attach(validated_response.model_dump_json(indent=2, ensure_ascii=False),
                      attachment_type=allure.attachment_type.JSON,
                      name="Validated verify login API response")


@allure.epic('API Testing')
@allure.feature('Verify login endpoint')
@allure.story('Invalid POST request without email parametres')
@allure.severity(allure.severity_level.CRITICAL)
def test_login_verify_invalid_request(api_session):
    """Тестируем POST запрос без параметра email на verify login endpoint"""

    with allure.step("Отправляем POST запрос для авторизации пользователя без параметра email в теле запроса."):
        response = api_session.post(f"{BASE_URL}/api/verifyLogin", data={"password": "1111"})

    with allure.step("Проверяем, что HTTP статус все равно 200 (особенность этого API)"):
        assert response.status_code == 200

    with allure.step("Валидируем структуру ответа об ошибке через Pydantic"):
        response_data = response.json()
        try:
            validated_response = APIError(**response_data)

            assert validated_response.responseCode == 400, f'Ожидаемый responseCode - 400, получили {validated_response.responseCode}'
            assert "Bad request" in validated_response.message, f"Ожидаемое сообщение - 'Bad request, email or password parameter is missing in POST request', а получили - {validated_response.message}"

        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации структуры ответа об ошибке:\n{e}")

        allure.attach(validated_response.model_dump_json(indent=2, ensure_ascii=False),
                      attachment_type=allure.attachment_type.JSON,
                      name="Validated verify login API response without email or password parameter")


@allure.epic('API Testing')
@allure.feature('Verify login endpoint')
@allure.story('Invalid DELETE request to verify login endpoint')
@allure.severity(allure.severity_level.NORMAL)
def test_login_verify_invalid_request_method(api_session):
    """Тестируем Delete запрос на verify login endpoint"""

    with allure.step("Отправляем DELETE запрос для авторизации пользователя без параметра email в теле запроса."):
        response = api_session.delete(f"{BASE_URL}/api/verifyLogin",
                                      data={"email": "test@mail.com", "password": "11111123"})

    with allure.step("Проверяем, что HTTP статус все равно 200 (особенность этого API)"):
        assert response.status_code == 200

    with allure.step("Валидируем структуру ответа об ошибке через Pydantic"):
        response_data = response.json()
        try:
            validated_response = APIError(**response_data)

            assert validated_response.responseCode == 405, f'Ожидаемый responseCode - 405, получили {validated_response.responseCode}'
            assert "method is not supported" in validated_response.message, f"Ожидаемое сообщение - 'This request method is not supported.', а получили - {validated_response.message}"

        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации структуры ответа об ошибке:\n{e}")

        allure.attach(validated_response.model_dump_json(indent=2, ensure_ascii=False),
                      attachment_type=allure.attachment_type.JSON,
                      name="Validated api response to Delete request on verify login endpoint")
