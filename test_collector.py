from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import json
from multiprocessing import Pool
import sqlite3
import time
import re


# link = 'https://vseapteki.ru/search/?query=Капли&page=1'
link1 = 'https://apteka-ot-sklada.ru/catalog?q=Капли&start=0'
# link2 = 'https://novosibirsk.asna.ru/search/?query=Капли&page=1'
# link3 = 'https://zdravcity.ru/search/?order=Y&what=Капли'

def webdr():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver_path = r'D:\Python\Diploma\third_party\chromedriver.exe'
    driver = webdriver.Chrome(
        executable_path=driver_path,
        options=options)
    return driver


driver = webdr()
try:
    # driver.get(url=link)
    driver.get(url=link1)
    # driver.get(url=link2)
    # driver.get(url=link3)
    items = driver.find_element_by_class_name('goods-grid__inner').get_attribute("outerHTML")
    soup = BeautifulSoup(items, 'lxml')
    inner_html = soup.find_all('div', class_='goods-card__price')
    price_list = []
    for item in inner_html:
        print(item)
    for inner in inner_html:
        price_list.append(inner.span.text)
    price_list = [price.strip() for price in price_list]
    print(price_list)
    driver.close()
    driver.quit()
except Exception as ex:
    print(ex)

'''
    print(inner_html)
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
'''
'''
    items = driver.find_element_by_class_name('cards-list-sort-filter ViewSearch__items').get_attribute("outerHTML")
    soup = BeautifulSoup(items, 'lxml')
    inner_html = soup.find_all('a', class_='pager-v3-item')
    # print(items)
    for i in inner_html:
        if i['href'] == 'javascript:void(0)':
            print(i['data-href'])
        else:
            print(i['href'])
'''
'''
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
'''
# рабочий вариант парсинга

'''
filename = 'src/links.json'
this_folder = os.path.dirname(os.path.abspath(__file__))
path_to_files = os.path.join(this_folder, filename)

with open(path_to_files, 'r') as f:
    data = json.load(f)
    filter_word = 'Капли'
    for i in range(len(data)):
        full_link = str(
            data[f'source{i + 1}']['host'] + str(data[f'source{i + 1}']['absolute path']).replace('*', filter_word, 1))
        print(full_link)
'''
'''


def work_pool(link, addlink):
    conn = sqlite3.connect('test_db.db')
    cur = conn.cursor()
    cur.execute(f'INSERT INTO table_name(col1,col2) VALUES(?,?)', [link, addlink])
    conn.commit()
    cur.close()
    conn.close()


def pool_handler():
    link = {'link0': 'heah', 'link1': 'hehehe', 'link2': 'huho'}
    add_data_to_pool = {'addlink0': 'addheah', 'addlink1': 'addhehehe', 'addlink2': 'addhuho'}
    with Pool(3) as pool:
        pool.starmap(work_pool, zip(link, add_data_to_pool))


if __name__ == '__main__':
    """conn = sqlite3.connect('test_db.db')
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE table_name(col1,col2)')"""
    # pool_handler()
    print([i for i in range(1, 5)])
'''
'''
links = ['link=sdasda=2', 'link=sdasda=3', 'link=sdasda=4', 'link=sdasda=5', 'link=sdasda=18', 'link=sdasda=19']
last_page = 0
links_base = ''
for i in links:
    breaking_sym = [i.start() for i in re.finditer('=', i)][-1] + 1
    page_num_in_link = i[breaking_sym:]
    print(page_num_in_link)
    links_base = i[:breaking_sym]
    print(links_base)
    page_num = int(page_num_in_link)
    if page_num > last_page:
        last_page = page_num
print(links_base)
restored_page_links = []
for i in range(1, last_page+1, 1):
    restored_page_links.append(links_base + str(i))
print(restored_page_links)
'''
'''
links = ['asjdnajsnjdanjsndjasnj123', 'asjdnajsnjdanjsndjasnj123', 'asjdnajsnjdanjsndjasnj123', 'asjdnajsnjdanjsndjasnj123', 'asjdnajsnjdanjsndjasnj123', 'asjdnajsnjdanjsndjasnj123']
conn = sqlite3.connect('./src/Links.db')
cursor = conn.cursor()
for link in links:
    cursor.execute(''''''INSERT INTO items (link) VALUES (?)'''''', (link,))
'''
'''
links = ['link1', 'link2', 'link3', 'link4']
data = {'source1': {'first': {'yes1': 'ooo'}, 'second': 'no1'}, 'source2': {'first': 'yes2', 'second': 'no2'}, 'source3': {'first': 'yes3', 'second': 'no3'}, 'source4': {'first': 'yes4', 'second': 'no4'}}
prep_data = [value['first'] for value in data.values()]
print(list(zip(links, prep_data)))
'''
'''
from src.database import DBConnection


with open('./Links.db', 'w+') as f:
    db = DBConnection()
    db.create_items_table()
    db.create_pages_links_table()
'''
'''
from itertools import zip_longest

items = ['0000', '0001', '0010']
names = ['0011', '0100', '0101']
price = ['0110', '0111']

print(list(zip_longest(items, names, price)))
'''