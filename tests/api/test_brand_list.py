import allure
import requests
from pydantic import ValidationError

from models.api_responses import APIResponse
from models.brand import Brand


@allure.epic('API Testing')
@allure.feature('GET requests')
@allure.story('GET brandslist testing')
@allure.severity(allure.severity_level.CRITICAL)
def test_get_brands_list():
    """Тестируем POST запрос к списку продуктов и валидируем структуру ответа через Pydantic"""

    with allure.step("Отправляем GET запрос к /api/brandsList"):
        response = requests.post('https://automationexercise.com/api/brandsList')

    with allure.step("Проверяем статус-код ответа"):
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

    with allure.step("Валидируем структуру ответа с помощью Pydantic-модели"):
        try:
            # МАГИЯ ЗДЕСЬ: мы пытаемся создать объект модели из сырого словаря.
            # Если хоть одно поле не совпадает (тип, длина, паттерн), будет выброшено ValidationError
            validated_response = APIResponse(**response.json())

            assert validated_response.responseCode == 200
            assert validated_response.message == 'This request method is not supported.'

            # Добавляем в отчет красивый, валидированный JSON для наглядности
            allure.attach(
                validated_response.model_dump_json(indent=2),
                name="Validated error response",
                attachment_type=allure.attachment_type.JSON
            )
        except ValidationError as e:
            # Если валидация не прошла, мы не просто падаем, а даем понятную ошибку
            raise AssertionError(f"Ошибка валидации структуры ответа через Pydantic:\n{e}")
