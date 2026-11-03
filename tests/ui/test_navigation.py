import time

import allure

from pages.home_page import HomePage

@allure.epic('UI Testing')
@allure.feature('Main page')
@allure.story('Page visualization checking')
@allure.severity(allure.severity_level.CRITICAL)
def test_main_page(page):
    """Тестируем отображение стартовой страницы www.automationexercise.com"""

    main_page = HomePage(page)
    with allure.step('Заходим на главную страницу www.automationexercise.com'):
        main_page.open()
        main_page.wait_for_page_load()

    with allure.step('Проверяем соответствие title главной  страницы.'):
        assert 'Automation Exercise'==main_page.get_title()

    with allure.step('Проверяем присутствие логотипа сайта.'):
        assert main_page.is_logo_visible()==True

        allure.attach(
            body=page.screenshot(),
            name="Start page",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step('Проверяем что слайдер товаров содержит товары.'):
        assert main_page.get_slider_count()>0

        allure.attach(
            body=main_page.rec_carousel_locator.screenshot(),
            name="Start page",
            attachment_type=allure.attachment_type.PNG
        )

@allure.epic('UI Testing')
@allure.feature('Navigation')
@allure.story('Navigation testing')
@allure.severity(allure.severity_level.CRITICAL)
def test_navigation(page):
    """Тестируем навигацию по вкладкам."""

    # Перехват запросов рекламы
    page.route("**/*", lambda route:
    route.abort() if any(ad_domain in route.request.url for ad_domain in
                         ["googleadservices", "googlesyndication", "doubleclick", "google_vignette"])
    else route.continue_()
               )

    home_page = HomePage(page)

    with allure.step('Заходим на главную страницу www.automationexercise.com'):
        home_page.open()
        home_page.wait_for_page_load()

    with allure.step('Нажимаем на кнопку навигации "Products"'):
        home_page.click_products()

    with allure.step('Проверяем что url изменился на /products'):
        assert page.url == 'https://www.automationexercise.com/products',f'https://www.automationexercise.com/products, а по факту {page.url}'

    with allure.step('Проверяем что заголовок страницы содержит "All Products"'):
        assert 'All Products' in home_page.get_title()

    with allure.step('Нажимаем на кнопку навигации "Cart"'):
        home_page.click_cart()

    with allure.step('Проверяем что url изменился на /view_cart'):
        assert page.url == 'https://www.automationexercise.com/view_cart', f'Ожидалось https://www.automationexercise.com/view_cart, а по факту {page.url}'

    with allure.step('Проверяем наличие элемента сообщения о пустой корзине.'):
        assert page.locator('span#empty_cart').is_visible()

    with allure.step('Нажимаем на кнопку навигации "Sign up/login"'):
        home_page.click_signup()

    with allure.step('Проверяем что url изменился на /login'):
        assert page.url == 'https://www.automationexercise.com/login', f'Ожидалось https://www.automationexercise.com/login, а по факту {page.url}'

    with allure.step('Проверяем наличие элемента формы ввода данных для перехода к регистрации.'):
        assert page.locator('div.signup-form').is_visible()










