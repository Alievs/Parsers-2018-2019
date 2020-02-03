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
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



def write_excel(datas):
    rb = open_workbook('./Maxus_right.xls')
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

        wb.save('./Maxus_right.xls')


def get_img(photo):
    tru_image = ''

    for pfile in photo:
        imag2 = pfile.split('/')[-1]
        # imag = "https://skleplamp.pl" + str(pli)
        image2 = 'Maxus_' + imag2
        p = requests.get(pfile)
        out = open(image2, "wb")
        out.write(p.content)
        out.close()
        tru_image += image2 + "|"

    return tru_image


def main():
    datas = []
    photo = []
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
    size = ''

    with open('D:\server\OSPanel\domains\parser1.loc\pars_data\data1.txt', 'r') as f:
        urlk = f.read().split()
        # for url in urlk:
        #     print(url)
        # print(len(urlk))

    # for i in range(1, 3):
    #     link = 'http://www.argon-lampy.pl/oferta/lampy-biurkowe/page/' + str(i) + '/'
    #     urlk.append(link)

    # urlk = ['I30418AC-GR']

    driver = webdriver.Chrome('D:\server\OSPanel\domains\parser1.loc\libs\selenium\chromedriver.exe')
    driver.set_window_size(500, 500)
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
    driver.execute_script(script, "https://maxus.com.ua/ru/")
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    for url in urlk[259:]:
        # driver.execute_script(script, "https://maxus.com.ua/ru/")
        # driver.switch_to.window(driver.window_handles[0])
        # driver.close()
        # driver.switch_to.window(driver.window_handles[0])
        inputEl = driver.find_element_by_xpath("//input[@id='search']")
        inputEl.send_keys(url)
        inputEl.send_keys(Keys.ENTER)
        try:
            elem = driver.find_element_by_xpath('//li[@class="item product product-item"]//a[3]')
            elem.send_keys(Keys.ENTER)
        except:
            driver.execute_script(script, "https://maxus.com.ua/ru/")
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue
        char = driver.find_element_by_xpath('//a[@id="tab-label-additional-title"]')
        char.send_keys(Keys.ENTER)
        time.sleep(3)
        # pinfo = driver.find_elements_by_xpath("//div[@class='full col span_4_of_5']/div[1]/div/div/a")
        # for tabl in pinfo:
        #     figs = tabl.get_attribute('href')
        #     kliks.append(figs)

        index = url

        # pli = driver.find_element_by_xpath("//div[@class='full col span_1_of_2']/a").get_attribute('href')
        # gi = get_img(pli)
        socle = "LED"
        tabel = driver.find_elements_by_xpath("//tr[@class='two-row']/td")
        for fik in tabel:
            label = fik.find_elements_by_xpath("span")[0].text
            value = fik.find_elements_by_xpath("span")[1].text
            if "Цвет корпуса" in label:
                color_stl = value
            if "Материал корпуса" in label:
                type_stl = value
            if "Габаритные размеры" in label:
                size = value
                height = size.split("*")[0]
                width = size.split("*")[1]
                heg = len(height)-1
                wid = len(width)-1
                height = height[:heg]
                width = width[:wid]
                try:
                    depth = size.split("*")[2]
                    dep = len(depth)-1
                    depth = depth[:dep]
                except:
                    depth = ''
        pli = driver.find_elements_by_xpath("//div[@class='fotorama__stage__shaft fotorama__grab']/div")
        for juc in pli:
            kiv = juc.get_attribute('href')
            photo.append(kiv)
        if not photo:
            kiv = driver.find_element_by_xpath("//div[@class='fotorama__stage__shaft']/div").get_attribute('href')
            photo.append(kiv)

        gi = get_img(photo)
        photo = []

        # print(color_stl + " ")
        # print(type_stl + " ")
        # print(height + " ")
        # print(width + " ")
        # print(depth + " ")

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


        # time.sleep(1)

    # f = open('D:\server\OSPanel\domains\parser1.loc\pars_data\data12.txt', 'w')
    # obj = ' '.join(kliks)
    # f.write(obj)

    driver.close()




if __name__ == '__main__':
    main()
