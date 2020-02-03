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
    rb = open_workbook('./Zuma_right.xls')
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

        wb.save('./Zuma_right.xls')


def get_img(photo):
    tru_image = ''

    for pfile in photo:
        imag2 = pfile.split('/')[-1]
        # imag = "https://skleplamp.pl" + str(pli)
        image2 = 'Zuma_' + imag2
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

    # urlk = ['MD1629-3A(copper)', 'RLX92350-20']

    driver = webdriver.Chrome('D:\server\OSPanel\domains\parser1.loc\libs\selenium\chromedriver.exe')
    driver.set_window_size(850, 200)
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
    #//div[@class='products viewphot s-row']/div[1]/div[1]/a[1]
    # driver.execute_script(script, "https://zuma-line.com.pl/pl/searchquery")
    # driver.switch_to.window(driver.window_handles[0])
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    for url in urlk[249:]:
        driver.execute_script(script, "https://zuma-line.com.pl/")
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        inputEl = driver.find_element_by_xpath("//input[@class='search__input']")
        inputEl.send_keys(url)
        inputEl.send_keys(Keys.ENTER)
        try:
            elem = driver.find_element_by_xpath("//div[@class='products viewphot s-row']/div[1]/div[1]/a[1]")
            elem.send_keys(Keys.ENTER)
        except:
            driver.execute_script(script, "https://zuma-line.com.pl/")
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue
        group = driver.find_element_by_xpath("//li[@class='current']/a").text
        # char = driver.find_element_by_xpath('//a[@id="tab-label-additional-title"]')
        # char.send_keys(Keys.ENTER)
        # time.sleep(3)
        index = url
        tabel = driver.find_elements_by_xpath("//table[@class='n54117_dictionary']/tbody/tr")
        i = 0
        for fik in tabel:
            try:
                label = fik.find_elements_by_xpath("//td[@class='n54117_item_a1']/span[1]")[i].text
                value = fik.find_elements_by_xpath("//td[@class='n54117_item_b1']/div[1]")[i].text
            except:
                label = ''
                value = ''
            i += 1
            if "Kolor" in label:
                color_stl = value
            if "Materiał" in label:
                type_stl = value
            if "Rodzaj trzonka" in label:
                socle = value
            if "Źródło światła" in label:
                jamp = value
                lamp = jamp.split("x")[0]
            if "Szerokość" in label:
                width = value
                width = re.findall(r'\d+', width)[0]
            if "Wysokość" in label:
                height = value
                height = re.findall(r'\d+', height)[0]
            if "Głębokość" in label:
                depth = value
                depth = re.findall(r'\d+', depth)[0]
        i = 0
        pli = driver.find_elements_by_xpath("//div[@class='smallgallery row']/div/ul/li/a")
        for juc in pli:
            kiv = juc.get_attribute('href')
            photo.append(kiv)
        if not photo:
            try:
                kiv = driver.find_element_by_xpath("//div[@class='mainimg productdetailsimgsize row']/a").get_attribute(
                    'href')
                photo.append(kiv)
            except:
                photo = []

        gi = get_img(photo)
        photo = []
        #
        # print(color_stl + " ")
        # print(type_stl + " ")
        # print(height + " ")
        # print(width + " ")
        # print(group + " ")
        #
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
