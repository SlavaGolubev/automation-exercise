import re

from playwright.async_api import expect

from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.products_list_locator = self.page.locator('div.productinfo')
        self.search_locator = self.page.locator('input#search_product')
        self.submit_locator = self.page.locator('button#submit_search')

    def get_products_count(self) -> int:
        products_count = self.products_list_locator.count()
        return products_count

    def search_product(self, query):
        self.search_locator.fill(query)
        self.submit_locator.click()
        self.page.wait_for_url("**/*search=*")

    def get_all_product_names(self) -> list:
        all_products_names = [product.locator('p').inner_text().strip() for product in self.products_list_locator.all()]
        return all_products_names

    def check_search_result(self, query):
        return any(query.lower() in product_name.lower() for product_name in self.get_all_product_names())



