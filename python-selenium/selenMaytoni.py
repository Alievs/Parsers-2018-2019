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
    rb = open_workbook('./Maytoni_right.xls')
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

        wb.save('./Maytoni_right.xls')


def get_img(photo):
    tru_image = ''

    for pfile in photo:
        imag2 = pfile.split('/')[-1]
        # imag = "https://skleplamp.pl" + str(pli)
        image2 = 'Maytoni_' + imag2
        p = requests.get(pfile)
        out = open(image2, "wb")
        out.write(p.content)
        out.close()
        tru_image += image2 + "|"

    return tru_image


def main():
    jink = []
    datas = []
    photo = []
    maker = ''
    country = ''
    tf = ''
    name = ''
    group = ''
    design = ''
    lamp = ''
    socle = 'LED'
    type_lamp = ''
    color_lamp = ''
    type_stl = ''
    color_stl = ''
    width = ''
    height = ''
    depth = ''
    urlk = []
    size = ''

# запись url  в файл
    with open('D:\server\OSPanel\domains\parser1.loc\pars_data\data2.txt', 'r') as f:
        urlk = f.read().split()
        for url in urlk:
            print(url)
        # print(len(urlk))

    # for i in range(1, 60):
    #     link = 'https://maytoni.ru/products/dekorativnyy_svet/?all=Y&PAGEN_1=' + str(i)
    #     urlk.append(link)

    # urlk = ['C007CW-01B', 'MIR003WL-L12CH']


 # работа скрипта
    driver = webdriver.Chrome('D:\server\OSPanel\domains\parser1.loc\libs\selenium\chromedriver.exe')
    driver.set_window_size(1100, 1000)
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
    driver.execute_script(script, "https://maytoni.ru/products/")
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    for url in urlk[838:]:#486
        # driver.execute_script(script, url)
        # driver.switch_to.window(driver.window_handles[0])
        # driver.close()
        # driver.switch_to.window(driver.window_handles[0])
        # choc = driver.find_elements_by_xpath("//div[@class='catalog-products']/a")
        # for trop in choc:
        #     vip = trop.get_attribute('href')
        #     print(vip)
        #     jink.append(vip)
        inputEl = driver.find_element_by_xpath("//input[@id='title-search-input']")
        inputEl.send_keys(url)
        inputEl.send_keys(Keys.ENTER)
        try:
            elem = driver.find_element_by_xpath("//div[@class='catalog-products']/a[1]")
            elem.send_keys(Keys.ENTER)
        except:
            driver.execute_script(script, "https://maytoni.ru/products/")
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue
        time.sleep(3)

        index = url
        try:
            name = driver.find_element_by_xpath(
                "//div[@class='product-short-info__item js-animate js-animated'][1]/a").text
        except:
            name = ''
        try:
            design = driver.find_element_by_xpath(
                "//div[@class='product-short-info__item js-animate js-animated'][3]/a").text
        except:
            design = ''
        try:
            telem = driver.find_element_by_xpath(
                "//button[@class='btn open-characteristics-button js-characteristics-button']")
            telem.send_keys(Keys.ENTER)
        except:
            tf = ''
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        tabel = driver.find_elements_by_xpath("//div[@class='product-characteristics-column']/div")
        for fik in tabel:
            label = fik.find_element_by_xpath("span").text
            value = fik.text
            # print(label)
            # print(value)
            if "Тип цоколя:" in label:
                socle = value.split("Тип цоколя:")[1].strip()
            if "Тип:" in label:
                group = value.split("Тип:")[1].strip()
            if "Цвет:" in label:
                color_stl = value.split("Цвет:")[1].strip()
            if "Материал арматуры:" in label:
                type_stl = value.split("Материал арматуры:")[1].strip()
            if "Кол-во ламп, шт.:" in label:
                lamp = re.search(r'\d+', value)[0]
            if "Цвет абажура:" in label:
                color_lamp = value.split("Цвет абажура:")[1].strip()
            if "Материал абажура:" in label:
                type_lamp = value.split("Материал абажура:")[1].strip()
            if "Макс. высота, мм:" in label:
                height = re.search(r'\d+', value)[0]
                heg = len(height) - 1
                height = height[:heg]
            if "Ширина, мм:" in label:
                width = re.search(r'\d+', value)[0]
                wid = len(width) - 1
                width = width[:wid]
            if "Диаметр, мм:" in label:
                width = re.search(r'\d+', value)[0]
                wid = len(width) - 1
                width = width[:wid]
                depth = width
            if "Глубина, мм:" in label:
                depth = re.search(r'\d+', value)[0]
                dep = len(depth) - 1
                depth = width[:dep]


        pli = driver.find_elements_by_xpath("//div[@class='product-gallery-wrapper']/a/img")
        for juc in pli:
            kiv = juc.get_attribute('src')
            photo.append(kiv)
        if not photo:
            pli = driver.find_elements_by_xpath("//div[@class='product-gallery-wrapper black-style']/a/img")
            for juc in pli:
                kiv = juc.get_attribute('src')
                photo.append(kiv)
        driver.execute_script("scroll(0, 0);")
        gi = get_img(photo)
        photo = []
        datas.append({'index': index,
                      'name': name,
                      'group': group,
                      'description': tf,
                      'maker': maker,
                      'country': country,
                      'design': design,
                      'lamp': lamp,
                      'socle': socle,
                      'color_lamp': color_lamp,
                      'type_lamp': type_lamp,
                      'color_stl': color_stl,
                      'type_stl': type_stl,
                      'width': width,
                      'heightm': height,
                      'depth': depth,
                      'photo': gi})
        write_excel(datas)


        # time.sleep(3)

    # f = open('D:\server\OSPanel\domains\parser1.loc\pars_data\data1.txt', 'w')
    # obj = ' '.join(jink)
    # f.write(obj)

    driver.close()


#DL023-2-01B

if __name__ == '__main__':
    main()
