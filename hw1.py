# Homework 1

"""
Task 1:
Источник: https://5ka.ru/special_offers/

Задача организовать сбор данных,
необходимо иметь метод сохранения данных в .json файлы
результат: Данные скачиваются с источника, при вызове метода/функции сохранения
в файл скачанные данные сохраняются в Json вайлы, для каждой категории товаров
должен быть создан отдельный файл и содержать товары исключительно
соответсвующие данной категории.

Пример структуры данных для файла:
{
"name": "имя категории",
"code": "Код соответсвующий категории (используется в запросах)",
"products": [{PRODUCT},  {PRODUCT}........] # список словарей товаров
соответсвующих данной категории
}
"""

# import necessary packages
import requests
import time
import os
import json

# create class Parse5
class Parse5:

    # domain and paths
    _main_domain = 'https://5ka.ru'
    _api_path_offers = '/api/v2/special_offers/'
    _api_path_categories = '/api/v2/categories/'

    # url, split into 2 parts
    _url_category_1 = 'https://5ka.ru/api/v2/special_offers/?store=&categories='
    _url_category_2 = '&ordering=&price_promo__gte=&price_promo__lte=&search='

    # parameters & headers
    params = {
        'records_per_page': 100,
        'page': 1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
        "Accept-Language": "en-US,en;q=0.5",
    }

    # define init
    def __init__(self):
        self.product = []
        self.categories_products = []

    # define download
    def download(self):
        params = {}
        url_category = self._main_domain + self._api_path_categories
        categories = requests.get(url_category, params=params, headers=self.headers).json()
        for i in categories:
            self.categories_products.append(i)
        for j in self.categories_products:
            j.update({'products': []})
            parent_group_code = j['parent_group_code']

            url = self._url_category_1 + parent_group_code + self._url_category_2

            params = self.params
            response = requests.get(url, params=params, headers=self.headers)

            if response.headers['Content-Type'] == 'application/json':
                products = response.json()

                for p in products['results']:
                    j['products'].append(p)
                time.sleep(0.5)
            else:
                break

    # define category_files
    def category_files(self):
        os.mkdir('category_files')
        for i in self.categories_products:
            parent_group_name = i['parent_group_name']
            file_path = os.path.join('category_files', '{0}.json'.format(parent_group_name))
            with open(file_path, 'w', encoding='UTF-8') as file:
                json.dump(i, file, ensure_ascii=False)

# do the run
if __name__ == '__main__':
    parser = Parse5()
    parser.download()
    parser.category_files()
    print(1)


