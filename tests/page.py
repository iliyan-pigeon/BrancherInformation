from extract_branches_info import extract_branches_info


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):

    def is_title_matches(self):
        return "Fibank" in self.driver.title
