from lxml import etree, html
from selenium import webdriver
import re

from lxml import etree, html
from time import sleep

from selenium import webdriver
import pandas as pd


def login(chrome):
    chrome.get('https://www.makeupalley.com/account/login.asp')
    chrome.find_element('xpath', "//*[@class='loginUsername form-control']").send_keys('ths')
    chrome.find_element('xpath', "//*[@class='loginPassword form-control']").send_keys('27022013')
    chrome.find_element('xpath', "//*[@class='login-submit button d-inline-block']").click()


def get_links():
    browser = webdriver.Firefox()
    login(browser)
    reviews = []

    for i in range(1, 97):
        link = f'https://www.makeupalley.com/product/searching?CategorySlug=face-moisturizer-skincare&NumberOfReviews=10&dsc=1&page={i}'
        browser.get(link)
        page = browser.page_source
        root = etree.fromstring(page, parser=html.HTMLParser())

        root.make_links_absolute(link)
        elements = root.xpath('//*[@class="image d-flex"]')
        reviews.extend(i.get('href') for i in elements)

    browser.close()
    with open('makeupalley.txt', 'w', encoding='utf8') as output:
        for line in reviews:
            output.write(line + '\n')


class Cream:
    def __init__(self, link):
        self.link = link
        self.name = link.split('/')[-3]
        self.brand = link.split('/')[-2]
        self.ingredients = []
        self.rating = 0

    def __repr__(self):
        return f'Cream {self.name} by {self.brand}\nrating {self.rating}\ningredients {self.ingredients}\n\n'

    def save(self):
        pass #marshmallow

    def csv_friendly(self, sep=u"\uE000"):
        return f'{self.brand}{sep}{self.name}{sep}{self.rating}{sep}{self.ingredients}\n'

    def get_rating(self, browser):
        browser.get(self.link)
        try:
            browser.find_element('xpath', '//*[@class="rating-value ml-1 mr-3"]')
        except:
            self.rating = -1
        else:
            page = browser.page_source
            root = etree.fromstring(page, parser=html.HTMLParser())
            self.rating = root.xpath('//*[@class="rating-value ml-1 mr-3"]')[0].text

    def get_ingredients(self, browser):

        browser.get(self.link)
        try:
            browser.find_element('xpath', '//*[@class="fa fa-ellipsis-h dots"]').click()
            sleep(1)
            browser.find_element('xpath', '//*[@data-event="show_ingredients_clicked"]').click()
            sleep(2)
            browser.find_element('xpath', '//*[@class="fa fa-pencil-square-o"]').click()
            sleep(2)
            page = browser.page_source
            root = etree.fromstring(page, parser=html.HTMLParser())
            self.ingredients = root.xpath('//*[@class="form-control edit-ingredients"]')[0].text.replace('\n', ' ')
        except:
            self.ingredients = ['not found']


def txt_to_csv(filename):
    links = pd.read_csv(filename, sep=u"\uE000", engine='python')
    links.to_csv(filename[:-3] + 'csv', index=None, header=None)


def get_data(link_file, output_file):
    with open(link_file) as _:
        links = _.read().splitlines()

    browser = webdriver.Firefox()
    login(browser)
    for i in range(631, len(links)):    #FIX
        c = Cream(links[i])
        c.get_ingredients(browser)
        c.get_rating(browser)
        with open(output_file, mode='a') as out:
            out.write(c.csv_friendly())
        if i % 100 == 0:
            print(i)
    txt_to_csv(output_file)


def get_missing_links():
    links = pd.read_csv('not_found.csv')['link']
    with open('missing_links.txt', mode='a') as missing:
        for link in links:
            missing.write(link + '\n')


#get_data('missing_links.txt', 'missing_results.txt')
