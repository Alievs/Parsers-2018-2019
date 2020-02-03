import requests
from bs4 import BeautifulSoup
import re
import lxml
from lxml import etree
import xlsxwriter
import xlrd
import xlwt
from xlutils.copy import copy
from xlrd import open_workbook
from xlwt import easyxf
import pandas as pd
import sqlite3
import os


def check_excel():
    j = 0
    hk = open_workbook('./a1.xls')
    r_sheet = hk.sheet_by_index(0)
    wb = copy(hk)
    w_sheet = wb.get_sheet(0)

    fields = ('index')

    rb = open_workbook('./a3.xls')
    sheet = rb.sheet_by_index(0)
    col1 = sheet.col_values(0)

    rb = open_workbook('./a2.xls')
    sheet = rb.sheet_by_index(0)
    col2 = sheet.col_values(0)


    for row, data in enumerate(col1):
        i = 1
        for rov, value in enumerate(col2):
            try:
                value = int(value)
            except:
                value = value

            try:
                data = int(data)
            except:
                data = data


            data = data.encode('utf-8').decode('utf-8-sig')
            if value == data:
                w_sheet.write(row, 2, i)
                print(str(value) +" col_2")
                print(str(data) +" col_1")
                j += i
                i += 1
                wb.save('./a1.xls')
    print(j)

def clear_excel():
    filepath = "D:\server\OSPanel\domains\parser1.loc\pars_data"
    filename = "adlex_done.xls"
    filePathFileName = filepath + "/" + filename
    outputPathFileName = filepath + "/cleaned_" + filename
    outputFileName = "cleaned_" + filename

    # pandas
    df = pd.read_excel(filePathFileName, header=0, nrows=14)

    # удалить пустые строки
    df.dropna(how='all', inplace=True)

    # заполнить пробелы в наших данных
    df.ffill(inplace=False)

    # создать базу данных sqlite и соединение с базой данных sqlite
    con = sqlite3.connect(":memory:")
    con.isolation_level = None
    cur = con.cursor()

    # создайте таблицу для наших данных в sqlite
    df.to_sql('example_data', con)

    # SQL-запрос для агрегирования наших данных
    df_pdsql = pd.read_sql_query(
        "SELECT col_A, col_B, col_C, col_D, col_E, col_F, col_G, col_H, col_I, col_J, col_K, col_L, col_M,"
        " col_N, col_O, col_P, col_Q FROM example_data", con)

    # напишите наш df в файл xlsx
    df_pdsql.to_excel(outputPathFileName, sheet_name='test', index=False)

    # сообщить пользователю, где находится файл
    print("Your new file is located in: " + outputPathFileName)

    # закрыть соединение с базой данных sqlite
    con.close()

def write_excel():
    hk = open_workbook('./a1.xls')
    r_sheet = hk.sheet_by_index(0)
    wb = copy(hk)
    w_sheet = wb.get_sheet(0)

    fields = ('index')

    rb = open_workbook('./a3.xls')
    sheet = rb.sheet_by_index(0)
    col1 = sheet.col_values(0)

    rb = open_workbook('./a2.xls')
    sheet = rb.sheet_by_index(0)
    col2 = sheet.col_values(0)

    for rov, value in enumerate(col1):
        value = value.encode('utf-8').decode('utf-8-sig')
        print(str(value) + " col_1")

        # w_sheet.write(rov, 3, value)
        # print(str(value) + " col_1")
        # wb.save('./a1.xls')







def main():
    li = clear_excel()


if __name__ == '__main__':
    main()
