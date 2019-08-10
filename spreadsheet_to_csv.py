# Written by Rory Austin id:28747194

import xlrd
import csv


def csv_from_xls(file, new_filename):
    '''This function takes a .xls file path and opens this workbook, from here it reads and writes each line to a csv file
    to be used inputting the data into a database.

    :param file: The file path to the .xls file that needs converting
    :param new_filename: the file path that the .csv file will be saved to
    :return: This function does not return an object
    '''
    try:
        # Open .xls workbook.
        print("[+] Opening Workbook")
        workbook = xlrd.open_workbook(file)
        sheet_names = workbook.sheet_names()
        sheet_name = sheet_names[0]  # Potential change, give option to input sheet_name and check for it.
        # Define the sheet for importing.
        sheet = workbook.sheet_by_name(sheet_name)
        # Create a new csv file with utf-8 encoding.
        print("[+] Creating file")
        csv_file = open(new_filename, 'w', encoding='utf-8-sig')
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        # Write each row to the csv file.
        for row_num in range(sheet.nrows):
            writer.writerow(sheet.row_values(row_num))
        # Close file
        csv_file.close()
        print("[+] CSV created")
    except:
        print("[-] Process failed")


# File paths for .xls and .csv files.
# data_file = r'C:\Users\Owner\Documents\photos\Project data\Monash_sample_VBA.xls'
# new_file = r'C:\Users\Owner\Documents\photos\Project data\data.csv'
# csv_from_xls(data_file, new_file)

