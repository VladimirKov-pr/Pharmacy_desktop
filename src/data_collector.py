from imports import *


def path_to_files(filename):
    """
    функция получения пути до файла
    :return string : путь до файла
    """
    this_folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(this_folder, filename)


def driver_options():
    """
    Метод настройки вебдрайвера Хром
    :return driver: настроенный вебдрайвер Хром
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver_path = '../third_party/chromedriver.exe'
        driver = webdriver.Chrome(
            executable_path=driver_path,
            options=options)
        return driver
    except Exception as ex:
        print(ex)
        return 0


def page_scroller(driver):
    """
    Метод получения html структуры страницы
    :param driver: вебдрайвер Хром
    """
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
    return driver


def get_pages(soup, pagestag, home_link, pages_class=''):
    """
    Метод получения ссылок страниц поиска
    :param (bs4.BeautifulSoup) soup: объект BeautifulSoup
    :param {} pagestag: тэги сайта для поиска элементов страниц
    :param pages_class: класс html контейнера для поиска ссылок страниц
    :param home_link: ссылка на главную страницу для конкатинации с ссылкой страницы поиска
    """
    try:
        pages = soup.find_all(pagestag, class_=pages_class)
        links = [(home_link + a['href'][1:]) for a in pages]
        return links
    except Exception as ex:
        print('Error : ', ex)


def restore_page_list(links, source_data):
    """
    Метод восстановления ссылок всех страниц. Собирает список ссылок по первой и последней ссылке, учитывая особенности
    источника
    :param [str] links: список собранных парсингом ссылок
    :param {} source_data: данные сайта ссылки для восстановления ссылок (особенность отсчета страниц,
    номер первой страницы поиска)
    """
    last_page = 0
    restored_page_links = []
    links_base = ''

    for link in links:
        breaking_sym = [link.start() for link in re.finditer('=', link)][-1] + 1
        page_num_in_link = link[breaking_sym:]
        links_base = link[:breaking_sym]
        page_num = int(page_num_in_link)
        if page_num > last_page:
            last_page = page_num

    for i in range(source_data['pages_feature'], last_page + 1, source_data['pages_counter']):
        restored_page_links.append(links_base + str(i))
    return restored_page_links


def get_items_data(soup, itemstag, homelink, item_name_tag, item_name_class, item_price_tag,
                   item_price_class, item_name_content, item_price_content, items_class=''):
    """
    Метод получения ссылок на товары страницы
    :param (bs4.BeautifulSoup) soup: объект BeautifulSoup
    :param {} itemstag: тэги сайта для поиска элементов товара
    :param items_class: класс html контейнера для поиска элементов товара
    :param homelink: ссылка на главную страницу для конкатинации с ссылкой товара
    :param item_name_tag: Тэг html элемента названия позиции
    :param item_name_class: Класс html элемента названия позиции
    :param item_price_tag: Тэг html элемента цены позиции
    :param item_name_content: путь до контента названия позиции структуры Html
    :param item_price_content: путь до контента цены позиции структуры Html
    :param item_price_class - Класс html элемента цены позиции
    """
    try:
        items = soup.find_all(itemstag, class_=items_class)
        names = soup.find_all(item_name_tag, class_=item_name_class)
        prices = soup.find_all(item_price_tag, class_=item_price_class)
        items_list = []
        names_list = []
        price_list = []

        for item in items:
            if item['href'] == 'javascript:void(0)':
                items_list.append(homelink + item['data-href'][1:])
            else:
                items_list.append(homelink + item['href'][1:])

        for name in names:
            if item_name_content == ".contents[0]":
                names_list.append(name.contents[0])
            elif item_name_content == ".span.contents[0]":
                names_list.append(name.span.contents[0])
            elif item_name_content == "['title']":
                names_list.append(name['title'])

        for price in prices:
            if item_price_content == ".span.text":
                try:
                    price_list.append(price.span.text)
                except Exception:
                    price_list.append('Временно нет на складе')
            elif item_price_content == ".contents[0]":
                if len(price.contents[0]):
                    price_list.append(price.contents[0])
                else:
                    price_list.append('Нет на складе')
        names_list = [name.strip() for name in names_list]
        price_list = [price.strip() for price in price_list]
        data = list(zip_longest(items_list, names_list, price_list))
        return data
    except Exception as ex:
        print('Error : ', ex)


def extract_souce_data(soucedata, action='SourceParsing'):
    """
    :param soucedata:
    :param action:
    :return *args
    """
    if action == 'SourceParsing':
        return soucedata['pages_container'], soucedata['pages'], soucedata['items_container'], \
               soucedata['items'], soucedata['pages_tag'], soucedata['items_tag'], soucedata['host'], \
               soucedata['item_name_tag'], soucedata['item_name_class'], soucedata['item_price_tag'], \
               soucedata['item_price_class'], soucedata['item_name_content'], soucedata['item_price_content']
    else:
        return soucedata['items_container'], soucedata['items'], soucedata['items_tag'], soucedata['host'], \
               soucedata['item_name_tag'], soucedata['item_name_class'], soucedata['item_price_tag'], \
               soucedata['item_price_class'], soucedata['item_name_content'], soucedata['item_price_content']


def pages_process_worker(pages_container, soucedata, tags):
    soup = BeautifulSoup(pages_container, 'lxml')
    pages_links = get_pages(soup, tags[0], tags[1], tags[2])
    restored_pages_links = restore_page_list(pages_links, soucedata)
    parsing_find_page_with_multiprocessing(restored_pages_links, soucedata, action='ItemsFromPages')


def items_process_worker(driver, items_container, action, tags, link=None):
    if action == 'SourceParsing':
        soup = BeautifulSoup(items_container, 'lxml')
        items = get_items_data(soup, tags[1], tags[2], tags[3], tags[4], tags[5],
                               tags[6], tags[7], tags[8], tags[9])
        db = database.DBConnection()
        db.insert_item_links(items)
    elif action == 'ItemsFromPages':
        items = []
        for page_link in link:
            try:
                driver.get(url=page_link)

                items_container = driver.find_element_by_class_name(tags[0]).get_attribute("outerHTML")
                if len(items_container):
                    soup = BeautifulSoup(items_container, 'lxml')
                    items += get_items_data(soup, tags[1], tags[2], tags[3], tags[4], tags[5],
                                            tags[6], tags[7], tags[8], tags[9])
            except NoSuchElementException as ex:
                print('Error: ', ex)
        db = database.DBConnection()
        db.insert_item_links(items)


def parsing_find_page_with_multiprocessing(link, soucedata, action='SourceParsing'):
    """
    :param link: преобразованная ссылка
    :param soucedata: данные сайта ссылки для поиска (тэги, классы)
    :param action: действие
    """

    if action == 'SourceParsing':
        driver = driver_options()
        driver.get(url=link)

        pages_container_tag, pages_class, items_container_tag, items_class, \
        pagestag, itemstag, homelink, item_name_tag, item_name_class, item_price_tag, item_price_class, \
        item_name_content, item_price_content = extract_souce_data(soucedata, 'SourceParsing')

        try:
            driver = page_scroller(driver)
            if len(pages_container_tag):
                pages_container = None
                try:
                    pages_container = driver.find_element_by_class_name(pages_container_tag).get_attribute("outerHTML")
                except Exception:
                    items_container = driver.find_element_by_class_name(items_container_tag).get_attribute("outerHTML")
                    items_process_worker(driver=driver, items_container=items_container, action='SourceParsing', tags=[
                        items_container_tag, itemstag, homelink, item_name_tag, item_name_class, item_price_tag,
                        item_price_class, item_name_content, item_price_content, items_class
                    ])
                if len(pages_container):
                    pages_process_worker(pages_container, soucedata, tags=[pagestag, homelink, pages_class])
            else:
                items_container = None
                try:
                    items_container = driver.find_element_by_class_name(items_container_tag).get_attribute("outerHTML")
                except:
                    pass
                if len(items_container):
                    items_process_worker(driver=driver, items_container=items_container, action='SourceParsing', tags=[
                        items_container_tag, itemstag, homelink, item_name_tag, item_name_class, item_price_tag,
                        item_price_class, item_name_content, item_price_content, items_class
                    ])
        except Exception as reqex:
            print('Request Error : ' + str(reqex))
        finally:
            driver.close()
            driver.quit()
    elif action == 'ItemsFromPages':
        items_container_tag, items_class, itemstag, homelink, item_name_tag, item_name_class, item_price_tag, \
            item_price_class, item_name_content, item_price_content = extract_souce_data(soucedata, 'ItemsFromPages')
        driver = driver_options()
        driver = page_scroller(driver)
        items_process_worker(driver=driver, items_container=None, action='ItemsFromPages', tags=[
            items_container_tag, itemstag, homelink, item_name_tag, item_name_class, item_price_tag,
            item_price_class, item_name_content, item_price_content, items_class
        ], link=link)


def grab_sites_url_pages():
    """
    функция чтения ссылок страниц, с которых будет производится поиск нужных ссылок товара
    :return: function: функция чтения данных сайтов с json файла
    """
    with open(path_to_files('links.json'), 'r') as f:
        return json.load(f)


def transform_links(souce_data, filter_word):
    """
    функция преобразования изначальных ссылок
    :param souce_data: данные источников (адрес до главной страницы, адрес до страницы поиска, тэги, классы)
    :param filter_word: ключевое слово поиска
    """
    full_link = []
    for i in range(1, (len(souce_data) + 1)):
        curent_linksdata = souce_data[f'source{i}']['prepare']
        full_link.append(str(
            curent_linksdata['host'] +
            str(curent_linksdata['absolute_path']).replace('*', filter_word, 1).replace('*', '1', 1)
        ))
    return full_link


def get_page_data(links, linksdata, poolnum):
    """
    функция, которая парсит данные по ссылке с сайта и пишет в словарь
    :param links: ссылки сайтов
    :param linksdata: данные ссылок(тэги, классы)
    :param poolnum:
    """
    prep_data = [value['prepare'] for value in linksdata.values()]
    args = zip(links, prep_data)
    with multiprocessing.Pool(poolnum) as pool:
        pool.starmap(parsing_find_page_with_multiprocessing, args)


def create_db_file():
    with open('./Links.db', 'w+'):
        db = database.DBConnection()
        db.create_items_table()
        db.create_pages_links_table()


def parse(keyword):
    """
    метод запуска методов модуля
    :param keyword: ключевое слово поиска
    """
    create_db_file()
    links = grab_sites_url_pages()
    transformed_links = transform_links(links, keyword)
    get_page_data(transformed_links, links, len(transformed_links))
