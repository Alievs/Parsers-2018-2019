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


def get_autf():

    with requests.Session() as session:

        url = 'http://www.artpolukraine.com.ua/auth/login/is_back/1'
        LOGIN = "nolimitsen@ukr.net"
        PASSWORD = "Zdfcbkbq25"
        SUBMIT = "увійти"
        _qf__loginForm = ""
        slovarb = {'login': 'nolimitsen@ukr.net',
                   'password': 'Zdfcbkbq25',
                   'submit': 'увійти',
                   '_qf__loginForm': ''}
        session.get(url)
        session.post(url, slovarb)
        url2 = "http://www.artpolukraine.com.ua/propozicz-ja/ndonez-ja-1/indonezja-maduro/"

        r = session.get(url2)
        r = r.text
        soup = BeautifulSoup(r, 'lxml')
        prince_1 = soup.find_all('div', class_='product ')[0].find('li', class_='price').find('span', class_='integer').text
        prince_2 = soup.find_all('div', class_='product ')[0].find('li',class_='price').find('span', class_='reminder').text
        prince = prince_1 + '' + prince_2
        print(prince + ' UAH')
        # print(v)

    return r

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    r = r.text.encode('ISO-8859-1').decode('utf-8')

    return r

def get_all_links():
    urls = []
    # limki = {'',
    #          ''}
    limki = {'http://www.artpolukraine.com.ua/propozicz-ja/r-zn-zobrazhennja/gob-rozdrukuwati-pin-up-girls/'}

    for value_list in limki:
        html = get_html(value_list)
        soup = BeautifulSoup(html, 'lxml')
        trili = soup.find_all('div', re.compile('product '))  # .find('a').get('href')

        for jkol in trili:
            sj = 'http://www.artpolukraine.com.ua' + jkol.find('a').get('href')

            urls.append(sj)

    return urls


def main():
    limki = get_all_links()

    with requests.Session() as session:

        url = 'http://www.artpolukraine.com.ua/auth/login/is_back/1'
        LOGIN = "nolimitsen@ukr.net"
        PASSWORD = "Zdfcbkbq25"
        SUBMIT = "увійти"
        _qf__loginForm = ""
        slovarb = {'login': 'nolimitsen@ukr.net',
                   'password': 'Zdfcbkbq25',
                   'submit': 'увійти',
                   '_qf__loginForm': ''}
        session.get(url)
        session.post(url, slovarb)

        for i, value_list in enumerate(limki, 1):
            r = session.get(value_list)
            r = r.text
            soup = BeautifulSoup(r, 'lxml')
            gi = get_img(r)
            prince_1 = soup.find_all('div', class_='product ')[0].find('li', class_='price').find('span',
                                                                                                  class_='integer').text
            prince_2 = soup.find_all('div', class_='product ')[0].find('li', class_='price').find('span',
                                                                                                  class_='reminder').text

            group = soup.find('ul', id='breadCrumbTrail').find_all('li')[-2].text
            print(group)





if __name__ == '__main__':
    main()




