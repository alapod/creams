from lxml import etree, html
from selenium import webdriver


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
        elements = root.xpath('//*[@class="item-name"]')
        reviews.extend(i.get('href') for i in elements)

    browser.close()
    with open('makeupalley.txt', 'w', encoding='utf8') as output:
        for line in reviews:
            output.write(line + '\n')
