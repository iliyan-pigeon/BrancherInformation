import unittest
from selenium import webdriver


class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://my.fibank.bg/EBank/public/offices")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
