import requests
import os
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
from selenium import webdriver
from selenium.webdriver.firefox.options import Options



def write_excel(datas):
    rb = open_workbook('./Argon_basic_right.xls')
    r_sheet = rb.sheet_by_index(0)
    wb = copy(rb)
    w_sheet = wb.get_sheet(0)

    print(r_sheet.nrows)

    fields = ('index', 'name', 'group',
              'description', 'maker', 'country',
              'design', 'lamp', 'socle', 'color_lamp',
              'type_lamp', 'color_stl', 'type_stl',
              'width', 'heightm', 'depth', 'photo')
    for row, data in enumerate(datas, start=1):
        # print(row)
        # print(data)
        for col, field in enumerate(fields):
            # print(col)
            # print(field)
            w_sheet.write(r_sheet.nrows, col, data[field])

        wb.save('./Argon_basic_right.xls')


def get_img(pli):
    tru_image = ''

    imag2 = pli.split('/')[-1]
    # imag = "https://skleplamp.pl" + str(pli)
    image2 = 'Argon_basic_' + imag2
    p = requests.get(pli)
    out = open(image2, "wb")
    out.write(p.content)
    out.close()
    tru_image += image2

    return tru_image


def main():
    datas = []
    kliks = []
    maker = ''#Nowodvorski
    country = ''#Польша
    tf = ''
    name = ''
    group = ''
    lamp = ''
    socle = ''
    type_lamp = ''
    color_lamp = ''
    type_stl = ''
    color_stl = ''
    width = ''
    height = ''
    depth = ''
    urlk = []

    with open('D:\server\OSPanel\domains\parser1.loc\pars_data\datall.txt', 'r') as f:
        urlk = f.read().split()
        # for url in urlk:
        #     print(url)
        # print(len(urlk))

    # for i in range(1, 3):
    #     link = 'http://www.argon-lampy.pl/oferta/lampy-biurkowe/page/' + str(i) + '/'
    #     urlk.append(link)

    # urlk = ['http://www.argon-lampy.pl/produkt/albatros-1148/']

    driver = webdriver.Chrome('D:\server\OSPanel\domains\parser1.loc\libs\selenium\chromedriver.exe')
    driver.set_window_size(100, 100)
    script = '''
    function new_tab(a, url){
                document.body.appendChild(a);
                a.setAttribute('href', url);
                a.dispatchEvent(
                    (function(e){
                        e.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, true, false, false, false, 0, null);
                        return e;
                    }(document.createEvent('MouseEvents'))
                    )
                );
    }
    new_tab(document.createElement('a'), arguments[0]);
    '''
    for url in urlk[1065:]:
        driver.execute_script(script, url)
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # pinfo = driver.find_elements_by_xpath("//div[@class='full col span_4_of_5']/div[1]/div/div/a")
        # for tabl in pinfo:
        #     figs = tabl.get_attribute('href')
        #     kliks.append(figs)

        index = driver.find_element_by_xpath("//div[@class='table']//tr[@class='active']/td[3]").text
        name = driver.find_element_by_xpath("//div[@class='p-desc col span_3_of_5']/ul[1]/li[5]").text
        name = name.replace('Rodzina: ', '')
        group = driver.find_element_by_xpath("//div[@class='p-desc col span_3_of_5']/ul[1]/li[6]").text
        group = group.replace('Rodzaj oprawy: ', '')
        chap = driver.find_element_by_xpath("//div[@class='p-desc col span_3_of_5']/ul[1]/li[4]").text
        chap = chap.replace('Źródło światła: ', '')
        chap = chap.lower()
        lamp = chap.split('x')[0]
        pli = driver.find_element_by_xpath("//div[@class='full col span_1_of_2']/a").get_attribute('href')
        try:
            gi = get_img(pli)
        except:
            gi =''
        if 'led' in chap:
            socle = "LED"
        else:
            socle = chap.split('x')[1].split('/')[0].replace(' ', '')
            socle = socle.upper()

        color_stl = driver.find_element_by_xpath("//div[@class='p-desc col span_3_of_5']/ul[1]/li[9]").text
        color_stl = color_stl.replace('Kolor: ', '')
        type_stl = driver.find_element_by_xpath("//div[@class='p-desc col span_3_of_5']/ul[1]/li[8]").text
        type_stl = type_stl.replace('Materiał wykonania: ', '')
        width = driver.find_element_by_xpath("//div[@class='p-desc col span_3_of_5']/ul[1]/li[3]").text
        try:
            width = re.search(r'\d+', width)[0]
            wid_n = len(width) - 1
            width = width[:wid_n]
        except:
            width = ''
        height = driver.find_element_by_xpath("//div[@class='p-desc col span_3_of_5']/ul[1]/li[2]").text
        try:
            height = re.search(r'\d+', height)[0]
            het_n = len(height) - 1
            height = height[:het_n]
        except:
            height = ''

        datas.append({'index': index,
                      'name': name,
                      'group': group,
                      'description': tf,
                      'maker': maker,
                      'country': country,
                      'design': tf,
                      'lamp': lamp,
                      'socle': socle,
                      'color_lamp': tf,
                      'type_lamp': tf,
                      'color_stl': color_stl,
                      'type_stl': type_stl,
                      'width': width,
                      'heightm': height,
                      'depth': depth,
                      'photo': gi})
        write_excel(datas)


        time.sleep(3)

    # f = open('D:\server\OSPanel\domains\parser1.loc\pars_data\data12.txt', 'w')
    # obj = ' '.join(kliks)
    # f.write(obj)

    driver.close()




if __name__ == '__main__':
    main()
