import os
import openpyxl
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from decouple import config
from dotenv import load_dotenv
load_dotenv()

def extract_branches_info():
    url = "https://my.fibank.bg/EBank/public/offices"

    driver = webdriver.Chrome()
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


def write_to_excel(branch_info_list):
    file_path = "C:/Users/User/OneDrive/Работен плот/fibank_branches.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    headers = ["Name", "Address", "Phone", "Saturday Hours", "Sunday Hours"]
    sheet.append(headers)

    for branch_info in branch_info_list:
        row = [branch_info[header] for header in headers]
        sheet.append(row)

    workbook.save(file_path)

    return file_path


def send_email(file_path):
    sender_email = config("SENDER_EMAIL")
    sender_password = config("SENDER_PASSWORD")
    receiver_email = input("Add the email receiver:")

    subject = "Fibank Branches Info"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    attachment = open(file_path, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)

    filename = os.path.basename(file_path)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())


if __name__ == "__main__":
    branches_info = extract_branches_info()

    excel_file_path = write_to_excel(branches_info)

    send_email(excel_file_path)
