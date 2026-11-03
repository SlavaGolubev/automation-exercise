import allure
import pytest

from models.user import RegistrationData
from pages.signup_page import RegistrationPage


@allure.epic('UI Testing')
@allure.feature('Registration')
@allure.story('Registration page testing')
@allure.severity(allure.severity_level.CRITICAL)
def test_signup(page):
    """Проверяем функционал регистрации."""

    registration_page = RegistrationPage(page)

    with allure.step('Заходим на страницу авторизации.'):
        registration_page.open('/login')

    with allure.step('Генерируем тестовые данные для регистрации.'):
        data_for_registration = RegistrationData.generate_data()

    with allure.step('Вводим имя и email для редиректа на страницу регистрации.'):
        registration_page.fill_signup_form(data_for_registration)

    with allure.step('Проверяем произошел ли редирект.'):
        assert registration_page.check_registration_page_open()

    with allure.step('Заполняем форму тестовыми данными и нажимаем кнопку создания аккаунта.'):
        registration_page.create_acc(data_for_registration)

    with allure.step('Проверяем успех создания аккаунта.'):
        allure.attach(page.screenshot(), attachment_type=allure.attachment_type.PNG, name="Account created")
        assert registration_page.check_success_acc()

@allure.epic('UI Testing')
@allure.feature('Registration')
@allure.story('Negative: test registration with existing email.')
@allure.severity(allure.severity_level.NORMAL)
def test_registration_with_existing_email(page):
    """Негативный тест при повторном использовании email для регаистрации."""

    registration_page = RegistrationPage(page)

    with allure.step('Заходим на страницу авторизации.'):
        registration_page.open('/login')

    with allure.step('Генерируем уникальные тестовые данные для регистрации.'):
        data_for_registration = RegistrationData.generate_data()

    with allure.step('Вводим имя и email для редиректа на страницу регистрации.'):
        registration_page.fill_signup_form(data_for_registration)

    with allure.step('Регистрируем аккаунт.'):
        registration_page.create_acc(data_for_registration)

    with allure.step('Проверяем успех создания первого аккаунта.'):
        allure.attach(page.screenshot(), attachment_type=allure.attachment_type.PNG, name="Account created")
        assert registration_page.check_success_acc(), "Первый аккаунт не был создан."

    with allure.step('Выходим из созданного аккаунта.'):
        page.goto('https://www.automationexercise.com/logout')

    with allure.step('Вводим зарегистрированный email повторно.'):
        registration_page.fill_signup_form(data_for_registration)

    with allure.step('Проверяем вывод предупреждения о том что email уже существует.'):
        allure.attach(page.screenshot(), attachment_type=allure.attachment_type.PNG, name="Email already exists message")
        assert registration_page.check_email_exist_message()

@allure.epic('UI Testing')
@allure.feature('Registration')
@allure.story('Negative: test registration with invalid email.')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize('invalid_email', ["not_an_email","missing_domain@","@missing_name.com"])
def test_registration_with_invalid_email(page,invalid_email):
    """Негативный тест использования некорректного email."""

    registration_page = RegistrationPage(page)
    data = RegistrationData.generate_data()

    with allure.step('Заходим на страницу авторизации.'):
        registration_page.open('/login')

    data.email = invalid_email

    with allure.step('Вводим имя и невалидный email.'):
        registration_page.fill_signup_form(data)

    with allure.step('Проверяем произошел ли редирект на страницу регистрации.'):
        assert '/login' in page.url


@allure.epic('UI Testing')
@allure.feature('Registration')
@allure.story('Negative: test registration with empty required fields.')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    'empty_field',
    ["password","firstname","lastname","address","city","state","zip","mobile_number"]
)
def test_registration_with_empty_required_field(page, empty_field):
    """Негативный тест при незаполнении обязательных полей регистрации."""

    registration_page = RegistrationPage(page)
    data = RegistrationData.generate_data()
    setattr(data, empty_field, "")

    with allure.step('Заходим на страницу авторизации.'):
        registration_page.open('/login')

    with allure.step('Вводим имя и email для редиректа на страницу регистрации.'):
        registration_page.fill_signup_form(data)

    with allure.step(f'Заполняем форму тестовыми данными c пустым полем {empty_field} и нажимаем кнопку создания аккаунта.'):
        registration_page.create_acc(data)

    with allure.step('Проверяем отказ в создании аккаунта при пустом обязательном поле.'):
        allure.attach(page.screenshot(), attachment_type=allure.attachment_type.PNG, name="Account created")
        assert page.url != 'https://www.automationexercise.com/account_created'






