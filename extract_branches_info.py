from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def extract_branches_info():
    url = "https://my.fibank.bg/EBank/public/offices"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    ul_locator = (By.CSS_SELECTOR, "#app .list-inline")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(ul_locator))

    html_source = driver.page_source

    soup = BeautifulSoup(html_source, "html.parser")

    ul_list_inline = soup.select("#app .list-inline")

    branches_info_list = []

    if ul_list_inline:
        li_elements = ul_list_inline[0].select("li.ng-scope")

        for li in li_elements:
            needed_info = li.select("div.margin-16")
            p = needed_info[0].find_all("p")

            if len(p) == 9:
                name = p[0].text
                address = p[1].text
                phone = p[8].text
                saturday_hours = p[6].text.replace(" ", "").replace("\n", "")
                sunday_hours = p[7].text.replace(" ", "").replace("\n", "")

                branch_info = {
                    "Name": name,
                    "Address": address,
                    "Phone": phone,
                    "Saturday Hours": saturday_hours,
                    "Sunday Hours": sunday_hours
                }

                branches_info_list.append(branch_info)

            elif len(p) == 7:
                name = p[0].text
                address = p[1].text
                phone = p[6].text
                saturday_hours = p[5].text.replace(" ", "").replace("\n", "")
                sunday_hours = "Closed"

                branch_info = {
                    "Name": name,
                    "Address": address,
                    "Phone": phone,
                    "Saturday Hours": saturday_hours,
                    "Sunday Hours": sunday_hours
                }

                branches_info_list.append(branch_info)

    driver.quit()

    return branches_info_list
