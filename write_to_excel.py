import openpyxl


def write_to_excel(branch_info_list):
    file_path = "C:/Users/User/Downloads/fibank_branches.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    headers = ["Name", "Address", "Phone", "Saturday Hours", "Sunday Hours"]
    sheet.append(headers)

    for branch_info in branch_info_list:
        row = [branch_info[header] for header in headers]
        sheet.append(row)

    workbook.save(file_path)

    return file_path
