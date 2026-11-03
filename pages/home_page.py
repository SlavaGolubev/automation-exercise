from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.logo_locator = self.page.locator('img[alt="Website for automation practice"]')
        self.home_nav_locator = self.page.locator('#header a[href="/"]')
        self.products_nav_locator = self.page.locator('#header a[href="/products"]')
        self.cart_nav_locator = self.page.locator('#header a[href="/view_cart"]')
        self.rec_carousel_locator = self.page.locator('div#recommended-item-carousel')
        self.features_items_locator = self.page.locator('div.features_items')
        self.signup_nav_locator = self.page.locator('#header a[href="/login"]')

    def click_products(self):
        self.products_nav_locator.click()

    def click_cart(self):
        self.cart_nav_locator.click()

    def click_signup(self):
        self.signup_nav_locator.click()

    def is_logo_visible(self) -> bool:
        return self.logo_locator.is_visible()

    def get_slider_count(self) -> int:
        sliders = self.rec_carousel_locator.locator('div.single-products').count()
        return sliders
