import requests
from bs4 import BeautifulSoup
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



def write_excel(datas):
    rb = open_workbook('./AArtpol_right.xls')
    r_sheet = rb.sheet_by_index(0)
    wb = copy(rb)
    w_sheet = wb.get_sheet(0)

    print(r_sheet.nrows)

    fields = ('index', 'name', 'group',
     'description', 'maker','country',
     'design', 'lamp', 'socle', 'color_lamp',
     'type_lamp','color_stl','type_stl',
     'width', 'heightm', 'depth', 'photo')
    for row, data in enumerate(datas, start=1):
        #print(row)
        #print(data)
        for col, field in enumerate(fields):
            #print(col)
            #print(field)
            w_sheet.write(r_sheet.nrows, col, data[field])

        wb.save('./AArtpol_right.xls')

def get_img(r):
    soup = BeautifulSoup(r, 'lxml')
    tru_image = ''
    bigJ = 'http://www.artpolukraine.com.ua' + soup.find('div', id='mainColumn').find('div', class_='rightColumn').find('div', class_='bigImageContainer').find('a').get('href')
    ima11 = bigJ.split('/')[-1]
    image22 = 'ArtPol_' + ima11
    p = requests.get(bigJ)
    out = open(image22, "wb")
    out.write(p.content)
    out.close()
    tru_image += image22 + '|'
    try:
        smlJ = soup.find('div', id='mainColumn').find('div', class_='rightColumn').find('div',
                                                                                        class_='images').find_all('a')
        for chiwors in smlJ:
            sec_img = 'http://www.artpolukraine.com.ua' + chiwors.get('href')
            ima1 = sec_img.split('/')[-1]
            image2 = 'ArtPol_' + ima1
            p = requests.get(sec_img)
            out = open(image2, "wb")
            out.write(p.content)
            out.close()
            tru_image += image2 + '|'
    except:
        tf =''

    return tru_image


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    r = r.text.encode('ISO-8859-1').decode('utf-8')

    return r

def get_all_links():
    urls = []
    # limki = {'',}
    # limki = {'',}
    limki = {'http://www.artpolukraine.com.ua/propozicz-ja/kartini-reprodukcz/reprodukcz-1/w-js-kowo-mors-kij-flot-4/'}
    # limki = {'http://www.artpolukraine.com.ua/propozicz-ja/kartini-reprodukcz/reprodukcz-1/gustaw-kl-mt-2/',
    #          'http://www.artpolukraine.com.ua/propozicz-ja/kartini-reprodukcz/reprodukcz-1/gustaw-kl-mt-2/storinka,1/'}
    # limki = {'http://www.artpolukraine.com.ua/propozicz-ja/kartini-reprodukcz/reprodukcz-1/dzhejms-d-n/',
    #          'http://www.artpolukraine.com.ua/propozicz-ja/kartini-reprodukcz/reprodukcz-1/dzhejms-d-n/storinka,1/'}
    # limki = {'http://www.artpolukraine.com.ua/propozicz-ja/kartini-reprodukcz/reprodukcz-1/z-rki/'}
    # limki = {'http://www.artpolukraine.com.ua/propozicz-ja/kartini-reprodukcz/reprodukcz-1/ditina/',
    #          'http://www.artpolukraine.com.ua/propozicz-ja/kartini-reprodukcz/reprodukcz-1/ditina/storinka,1/'}
    # limki = {'http://www.artpolukraine.com.ua/propozicz-ja/kartini-reprodukcz/reprodukcz-1/dika-priroda/',
    #          'http://www.artpolukraine.com.ua/propozicz-ja/kartini-reprodukcz/reprodukcz-1/dika-priroda/storinka,1/',
    #          'http://www.artpolukraine.com.ua/propozicz-ja/kartini-reprodukcz/reprodukcz-1/dika-priroda/storinka,2/'}









    for value_list in limki:
        html = get_html(value_list)
        soup = BeautifulSoup(html, 'lxml')
        trili = soup.find_all('div', re.compile('product '))  # .find('a').get('href')

        for jkol in trili:
            sj = 'http://www.artpolukraine.com.ua' + jkol.find('a').get('href')

            urls.append(sj)

    return urls


def main():
    datas = []

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

    limki = get_all_links()

    with requests.Session() as session:

        url = 'http://www.artpolukraine.com.ua/auth/login/is_back/1'

        slovarb = {'login': 'nolimitsen@ukr.net',
                   'password': 'Zdfcbkbq25',
                   'submit': 'увійти',
                   '_qf__loginForm': ''}
        session.get(url)
        session.post(url, slovarb)

        for i, value_list in enumerate(limki, 1):
            html = session.get(value_list)
            html = html.text.encode('ISO-8859-1').decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            gi = get_img(html)
            group = soup.find('ul', id='breadCrumbTrail').find_all('li')[-2].text
            name = soup.find('div', id='mainColumn').find('h3').text
            dargh = soup.find('p', class_='symbol').find('span').text
            index = re.findall('(\d+)', dargh)[0]
            try:
                size = soup.find('div', id='mainColumn').find('ul').find('li', class_='size').text
            except:
                size = ''
            try:
                hegm = size.split('x')[0]
                height = re.findall('(\d+)', hegm)[0]
            except:
                try:
                    hegm = size.split(',')[0]
                    height = re.findall('(\d+)', hegm)[0]
                except:
                    try:
                        hegm = size.split('/')[0]
                        height = re.findall('(\d+)', hegm)[0]
                    except:
                        tf = ''
            try:
                widt = size.split('x')[1]
                width = re.findall('(\d+)', widt)[0]
            except:
                try:
                    widt = size.split(',')[1]
                    width = re.findall('(\d+)', widt)[0]
                except:
                    try:
                        widt = size.split('/')[1]
                        width = re.findall('(\d+)', widt)[0]
                    except:
                        tf = ''
            try:
                type = soup.find('div', id='mainColumn').find('ul').find('li', class_='materials').text
                type_stl = type.split('матеріал')[1]
            except:
                tf = ''
            time.sleep(2)


            try:
                color = soup.find('div', id='mainColumn').find('ul').find('li', class_='color').text
                color_stl = color.split('колір')[1]
            except:
                tf = ''
            try:
                dept = size.split('x')[2]
                depth = re.findall('(\d+)', dept)[0]
            except:
                try:
                    dept = size.split(',')[2]
                    depth = re.findall('(\d+)', dept)[0]
                except:
                    try:
                        dept = size.split('/')[2]
                        depth = re.findall('(\d+)', dept)[0]
                    except:
                        depth = ''


            prince_1 = soup.find('div', id='mainColumn').find('ul').find('li', class_='price').find('span', class_='integer').text
            prince_2 = soup.find('div', id='mainColumn').find('ul').find('li', class_='price').find('span', class_='reminder').text
            prince = prince_1 + '' + prince_2

            datas.append({'index': index,
                          'name': name,
                          'group': group,
                          'description': tf,
                          'maker': tf,
                          'country': tf,
                          'design': tf,
                          'lamp': tf,
                          'socle': prince,
                          'color_lamp': tf,
                          'type_lamp': tf,
                          'color_stl': color_stl,
                          'type_stl': type_stl,
                          'width': width,
                          'heightm': height,
                          'depth': depth,
                          'photo': gi})

            write_excel(datas)






if __name__ == '__main__':
    main()