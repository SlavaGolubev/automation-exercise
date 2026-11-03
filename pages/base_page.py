

class BasePage:

    def __init__(self, page):
        self.page = page
        self.url = 'https://www.automationexercise.com/'

    def open(self, path: str =''):
        full_url = self.url + path.lstrip('/')
        self.page.goto(full_url)

    def get_title(self):
        return self.page.title()

    def wait_for_page_load(self):
        self.page.wait_for_load_state('domcontentloaded')
