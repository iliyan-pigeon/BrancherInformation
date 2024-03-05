from extract_branches_info import extract_branches_info
from send_mail import send_email
from write_to_excel import write_to_excel

if __name__ == "__main__":
    branches_info = extract_branches_info()

    excel_file_path = write_to_excel(branches_info)

    send_email(excel_file_path)
