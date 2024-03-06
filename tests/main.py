import os
import unittest

import openpyxl
from selenium import webdriver

import extract_branches_info
import page
from write_to_excel import write_to_excel


class FibankSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://my.fibank.bg/EBank/public/offices")

    def test_title(self):
        main_page = page.MainPage(self.driver)
        assert main_page.is_title_matches()

    def test_is_extract_branches_info_return_something(self):
        value = extract_branches_info
        assert value is not []

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
