import allure
import pytest
from playwright.sync_api import Page

from pages.products_page import ProductPage


@allure.epic('UI Testing')
@allure.feature('Products page')
@allure.story('Product search testing')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize('product_name, expected_search_result',
                         [('winter top', True), ('Dress', True), ('Shoes', False)],
                         ids=['winter top - positive', 'Dress - positive', 'Shoes - negative'])
def test_search_product_success(page: Page, product_name, expected_search_result):
    """Проверяем фунцкционал поиска товара."""

    # Перехват запросов рекламы
    page.route("**/*", lambda route:
    route.abort() if any(ad_domain in route.request.url for ad_domain in
                         ["googleadservices", "googlesyndication", "doubleclick", "google_vignette"])
    else route.continue_()
               )

    products_page = ProductPage(page)

    with allure.step('Заходим на страницу товаров.'):
        products_page.open('/products')

    with allure.step('Проверяем осуществился ли переход'):
        assert "All Products" in products_page.get_title()

    with allure.step('Вводим название товара либо его часть и запускаем поиск.'):
        products_page.search_product(product_name)

    with allure.step('Проверяем результат поиска.'):
        allure.attach(page.screenshot(), attachment_type=allure.attachment_type.PNG, name="Search result")
        assert products_page.check_search_result(product_name) is expected_search_result
