import random

from faker import Faker
from playwright.sync_api import Page

from pages.base_page import BasePage



class RegistrationPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.name_locator = self.page.locator("input[data-qa='signup-name']")
        self.email_locator = self.page.locator("input[data-qa='signup-email']")
        self.submit_button_locator = self.page.locator("button[data-qa='signup-button']")
        self.signup_nav_locator = self.page.locator("#header a[href='/login']")
        self.registration_title_locator = self.page.locator("form[action='/signup'] b")

        self.male = self.page.locator("div.radio-inline label[for='id_gender1']")
        self.female = self.page.locator("div.radio-inline label[for='id_gender2']")
        self.name = self.page.locator("[data-qa='name']")
        self.email = self.page.locator("[data-qa='email']")
        self.password = self.page.locator("[data-qa='password']")
        self.day = self.page.locator("[data-qa='days']")
        self.month = self.page.locator("[data-qa='months']")
        self.year = self.page.locator("[data-qa='years']")
        self.newsletter = self.page.locator("input#newsletter")
        self.offersletter = self.page.locator("input#optin")
        self.firstname = self.page.locator("[data-qa='first_name']")
        self.lastname = self.page.locator("[data-qa='last_name']")
        self.company = self.page.locator("[data-qa='company']")
        self.address = self.page.locator("[data-qa='address']")
        self.address2 = self.page.locator("[data-qa='address2']")
        self.country = self.page.locator("[data-qa='country']")
        self.state = self.page.locator("[data-qa='state']")
        self.city = self.page.locator("[data-qa='city']")
        self.zipcode = self.page.locator("[data-qa='zipcode']")
        self.mobile = self.page.locator("[data-qa='mobile_number']")
        self.create_acc_button = self.page.locator("[data-qa='create-account']")
        self.acc_created = self.page.locator("[data-qa='account-created']")
        self.email_exist_message = self.page.locator("form[action='/signup'] p[style='color: red;']")
        self.logout = self.page.locator("[action='/login']")

    def signup_nav_click(self):
        self.signup_nav_locator.click()

    def fill_signup_form(self, data):
        self.name_locator.fill(data.name)
        self.email_locator.fill(data.email)
        self.submit_button_locator.click()

    def check_registration_page_open(self) -> bool:
        return 'address information' in self.registration_title_locator.inner_text().lower()

    def create_acc(self, data):

        if data.title=='Mr.':
            self.male.check()
        else:
            self.female.check()
        self.password.fill(data.password)
        self.day.select_option(data.birth_day)
        self.month.select_option(data.birth_month)
        self.year.select_option(data.birth_year)
        if data.newsletter:
            self.newsletter.check()
        if data.offersletter:
            self.offersletter.check()
        self.firstname.fill(data.first_name)
        self.lastname.fill(data.last_name)
        self.company.fill(data.company)
        self.address.fill(data.address1)
        if data.address2:
            self.address2.fill(data.address2)
        self.country.select_option(data.country)
        self.state.fill(data.state)
        self.city.fill(data.city)
        self.zipcode.fill(data.zipcode)
        self.mobile.fill(data.mobile_number)

        self.create_acc_button.click()

    def check_success_acc(self) -> bool:
        return "ACCOUNT CREATED" in self.acc_created.inner_text()

    def check_email_exist_message(self) -> bool:
        return "Email Address already exist!" in self.email_exist_message.inner_text()




