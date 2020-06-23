import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


def search():
    try:
        browser.get('https://www.tntsupermarket.com/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#all-page-location'))
        )
        input.send_keys('8 Mango Dr North York, ON, M2K 2G1')
        select = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#select-location > div > div > div.view-wrapper > '
                                                         'div.bottom > div > ul > li:nth-child(1) > span.text'))
        )
        select.click()
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#select-location > div > div > div.view-wrapper > div.bottom > div > button'))
        )
        submit.click()
        fresh_link = browser.find_element_by_xpath('//*[@id="ui-id-4"]')
        url = fresh_link.get_attribute('href')
        print(url)
        time.sleep(8)
        browser.get(url)
        # no item num relative
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#layer-product-list > div:nth-child(3) > '
                                                                            'div.pages > ul > li:nth-child(8) > a > '
                                                                            'span:nth-child(2)')))
        get_products()
        return total.text
    except TimeoutException:
        return search()


def next_page(page_number):
    try:
        browser.get('https://www.tntsupermarket.com/fresh-frozen.html?p=' + page_number)
        current_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#layer-product-list > '
                                                                                     'div:nth-child(3) > div.pages > ul >'
                                                                                     ' li.item.current')))
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#layer-product-list > '
                                                                'div.products.wrapper.grid.products-grid > ol '
                                                                '.item.product.product-item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#layer-product-list > div.products.wrapper.grid.products-grid > ol .item.product.product-item').items()
    for item in items:
        product = {
            'image': item.find('.product-item-info .product-image-photo').attr('src'),
            'price': item.find('.price').text(),
            'title': item.find('.product-item-link').text()
        }
        print(product)



def main():
    total = search()
    total = int(total)
    for i in range(2, total + 1):
        next_page(str(i))


if __name__ == '__main__':
    main()