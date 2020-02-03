import requests
from bs4 import BeautifulSoup
import time
import re
import lxml
from lxml import etree
import xlsxwriter
import xlrd
import xlwt
from xlutils.copy import copy
from xlrd import open_workbook
from xlwt import easyxf
import csv



def get_img(html):
    soup = BeautifulSoup(html, 'lxml')
    tru_image = ''
    img2 = soup.find('ul', class_='carousel-image-m').find_all('li')
    for blug in img2:
        ig2 = 'https://www.eichholtz.com' + blug.find('img').get('data-src')
        ima1 = ig2.split('/')[-1]
        ima2 = ig2.split('/')[-2]
        image2 = ima2 + '_' + ima1
        p = requests.get(ig2)
        out = open(image2, "wb")
        out.write(p.content)
        out.close()
        tru_image += image2 + '|'

    return tru_image

def check_excel():
    hk = open_workbook('./a2.xls')
    r_sheet = hk.sheet_by_index(0)
    wb = copy(hk)
    w_sheet = wb.get_sheet(0)

    fields = ('index')

    rb = open_workbook('./artpol_(all).xls')
    sheet = rb.sheet_by_index(0)
    col1 = sheet.col_values(0)

    rb = open_workbook('./a3.xls')
    sheet = rb.sheet_by_index(0)
    col2 = sheet.col_values(0)

    # print(len(list(set(col2))))

    # for row, data in enumerate(col1):
    #     w_sheet.write(row, 1, data)
    #     wb.save('./e2.xls')


    for row, data in enumerate(col2):
        i = 1
        for rov, value in enumerate(col1):
            if value == data:
                w_sheet.write(row, 2, i)
                print(value)
                i += 1
                wb.save('./a2.xls')

def main():
    li = check_excel()







if __name__ == '__main__':
    main()