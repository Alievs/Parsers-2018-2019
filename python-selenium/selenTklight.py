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
    rb = open_workbook('./TK_Light_right.xls')
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
        for col, field in enumerate(fields):
            w_sheet.write(r_sheet.nrows, col, data[field])

        wb.save('./TK_Light_right.xls')


def get_img(photo):
    tru_image = ''

    for pfile in photo:
        imag2 = pfile.split('/')[-1]
        # imag = "https://skleplamp.pl" + str(pli)
        image2 = 'TK_Light_' + imag2
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


    # запись url  в файл
    with open('D:\server\OSPanel\domains\parser1.loc\pars_data\datall.txt', 'r') as f:
        urlk = f.read().split()
        # for url in urlk:
        #     print(url)
        # print(len(urlk))

    # for i in range(1, 6):
    #     link = 'https://tk-lighting.eu/product-category/%D0%B0%D1%80%D0%BC%D0%B0%D1%82%D1%83%D1%80%D0%B0/%D0%BD%D0%BE%D1%87%D1%8C/?product-page=' + str(i)
    #     urlk.append(link)

    # urlk = ['https://tk-lighting.eu/produkt/kinkiet-lampa-sufitowa-aga-6/',
    #         'https://tk-lighting.eu/produkt/lampa-scienna-sufitowa-quadro-13/']

    # работа скрипта
    driver = webdriver.Chrome('D:\server\OSPanel\domains\parser1.loc\libs\selenium\chromedriver.exe')
    driver.set_window_size(300, 300)
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
    for url in urlk[630:]:
        driver.execute_script(script, url)
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # choc = driver.find_elements_by_xpath("//div[@class='card-img-top']/a[1]")
        # for trop in choc:
        #     vip = trop.get_attribute('href')
        #     jink.append(vip)

        try:
            index = driver.find_element_by_xpath("//span[@class='sku']").text
        except:
            continue
        group = driver.find_element_by_xpath("//h1").text
        if "KINKIET" in group:
            group = 'Бра і настінні'
        if "LAMPA ŚCIENNA" in group:
            group = 'Світильники стельові'
        if "LAMPA WISZĄCA" in group:
            group = 'Світильники стельові'
        if "LAMPA SUFITOWA" in group:
            group = 'Світильники стельові'
        if "LAMPA PODŁOGOWA" in group:
            group = 'Торшери'
        if "LAMPA BIURKOWA" in group:
            group = 'Настільні лампи'

        tabel = driver.find_elements_by_xpath("//table[@class='shop_attributes']/tbody/tr")
        for fik in tabel:
            label = fik.find_element_by_xpath("th").text
            value = fik.find_element_by_xpath("td").text
            if "Тип цоколя" in label:
                socle = value
            if "материал" in label:
                type_stl = value
            if "Цвет рамки" in label:
                color_stl = value
            if "Размеры" in label:
                size = value
                width = size.split("×")[0]
                height = size.split("×")[1]
                width = width.split()[0]
                height = height.split()[0]
                heg = len(height)-1
                wid = len(width)-1
                height = height[:heg]
                width = width[:wid]
                try:
                    depth = size.split("×")[2]
                    depth = re.search(r'\d+', depth)[0]
                    dep = len(depth) - 1
                    depth = width[:dep]
                except:
                    depth = ''

        pli = driver.find_elements_by_xpath("//div[@class='woocommerce-product-gallery__image flex-active-slide']/a")
        for juc in pli:
            kiv = juc.get_attribute('href')
            photo.append(kiv)
        gi = get_img(photo)
        photo = []
        # print(color_stl + " ")
        # print(type_stl + " ")
        # print(width + " ")
        # print(height + " ")
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


    # f = open('D:\server\OSPanel\domains\parser1.loc\pars_data\data5.txt', 'w')
    # obj = ' '.join(jink)
    # f.write(obj)

    driver.close()




if __name__ == '__main__':
    main()
