# Written by Rory Austin id:28747194

import xlrd
import csv


# This is a helper file that takes an excel workbook and converts it into a csv file.
# Used in 'populate_database.py' file.


def csv_from_xls(file, new_filename):
    '''This function takes a .xls file path and opens this workbook, from here it reads and writes each line to a csv file
    to be used inputting the data into a database.

    :param file: The file path to the .xls file that needs converting
    :param new_filename: the file path that the .csv file will be saved to
    :return: This function does not return an object
    '''
    # Open .xls workbook.
    print("[+] Opening Workbook")
    workbook = xlrd.open_workbook(file)
    sheet_names = workbook.sheet_names()
    sheet_name = sheet_names[0]  # Potential change, give option to input sheet_name and check for it.
    # Define the sheet for importing.
    sheet = workbook.sheet_by_name(sheet_name)
    # Create a new csv file with utf-8 encoding.
    csv_file = open(new_filename, 'w', encoding='utf-8-sig')
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    # Write each row to the csv file.
    for row_num in range(sheet.nrows):
        writer.writerow(sheet.row_values(row_num))
    # Close file
    csv_file.close()


