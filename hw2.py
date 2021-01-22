# Homework 2

"""
Task 1

Источник https://magnit.ru/promo/?geo=moskva
Необходимо собрать структуры товаров по акции и сохранить их в MongoDB
пример структуры и типы обязательно хранить поля даты как объекты datetime
{
    "url": str,
    "promo_name": str,
    "product_name": str,
    "old_price": float,
    "new_price": float,
    "image_url": str,
    "date_from": "DATETIME",
    "date_to": "DATETIME",
}
"""

# Import of the necessary libraries
import os
import time
import requests
import bs4
from urllib.parse import urljoin
from pymongo import MongoClient
import re
import datetime

# Url & Client
url = 'https://magnit.ru/promo/?geo=moskva'
db_client = MongoClient(os.getenv('MONGO_DB_URL'))


# Create a class for errors
class Error(Exception):

    # Define init
    def __init__(self, text):
        self.text = text


# Create a class to parse the Magnit website
class MagnitParse:

    # Define init
    def __init__(self, start_url, db_client):
        self.start_url = start_url
        self.collection = db_client['gb_parse_12']['magnit']

    # todo create an url request

    # Define the response
    @staticmethod
    def __get_response(url: str, **kwargs) -> requests.Response:
        while True:
            try:
                response = requests.get(url, **kwargs)
                if response.status_code == 200:
                    return response
                raise Error(f'{response.status_code}')
            except (requests.exceptions.HTTPError,
                    requests.exceptions.ConnectTimeout,
                    Error):
                time.sleep(0.5)

    # todo get the soup

    # Define the soup
    @staticmethod
    def __get_soup(response: requests.Response) -> bs4.BeautifulSoup:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        return soup

    # Define run
    def run(self):
        page_soup = self.__get_soup(self.__get_response(self.start_url))
        for product in self.__get_product(page_soup):
            self.save(product)

    # todo get the data out of the soup
    def __get_product(self, soup: bs4.BeautifulSoup):
        catalog = soup.find('div', attrs={'class': 'сatalogue__main'})
        for tag_product in catalog.find_all('a', recursive=False):
            yield self._product_parse(tag_product)

    # Define promo_name
    @staticmethod
    def __get_promo_name(tag_product):
        try:
            promo_name = [e.text for e in tag_product.find(
                'div', attrs={'class': 'card-sale__name'}).descendants if e.name == 'p']
        except AttributeError:
            promo_name = ['No name!']
        return promo_name[0]

    # Define product_name
    @staticmethod
    def __get_product_name(tag_product):
        try:
            product_name = [e.text for e in tag_product.find(
                'div', attrs={'class': 'card-sale__title'}).descendants if e.name == 'p']
        except AttributeError:
            product_name = ['нет названия товара!']
        return product_name[0]

    # Define old price
    @staticmethod
    def __get_old_price(tag_product):
        try:
            price = tag_product.find('div', attrs={'class': 'label__price_old'})
            price_integer = price.find('span', attrs={'class': 'label__price-integer'})
            price_decimal = price.find('span', attrs={'class': 'label__price-decimal'})
            price_str = f'{price_integer.text},{price_decimal.text}'
            old_price = float(re.sub(r'[^0-9\.]', '', price_str))
        except AttributeError:
            old_price = None
        return old_price

    # Define new price
    @staticmethod
    def __get_new_price(tag_product):
        try:
            price = tag_product.find('div', attrs={'class': 'label__price_new'})
            price_integer = price.find('span', attrs={'class': 'label__price-integer'})
            price_decimal = price.find('span', attrs={'class': 'label__price-decimal'})
            price_str = f'{price_integer.text},{price_decimal.text}'
            new_price = float(re.sub(r'[^0-9\.]', '', price_str))
        except AttributeError:
            new_price = None
        return new_price

    # Define image url
    def __get_image_url(self, tag_product):
        try:
            tag_image = tag_product.find('img')
            image_url = urljoin(self.start_url, tag_image.get('data-src'))
        except AttributeError:
            image_url = None
        return image_url

    # Define data from
    @staticmethod
    def __get_data_from(tag_product):
        date_list_str = []
        sample_date = {
            "января": 1,
            "февраля": 2,
            "марта": 3,
            "апреля": 4,
            "мая": 5,
            "июня": 6,
            "июля": 7,
            "августа": 8,
            "сентября": 9,
            "октября": 10,
            "ноября": 11,
            "декабря": 12,
        }
        try:
            date_str = tag_product.find('div', attrs={'class': 'card-sale__date'})
            for tag in date_str.find_all('p', recursive=False):
                text = tag.text
                text_split = text.split()
                text_replace = ['с', 'до', 'Только']
                text_date = ' '.join(i for i in text_split if i not in text_replace)
                text_date_split = text_date.split()
                month_in_text_date = text_date_split[1]
                month_in_sample_date = sample_date[month_in_text_date]
                text_date_split[1] = str(month_in_sample_date)
                text_date_join = ''.join(text_date_split)
                date = f'{text_date_join}2020'
                date_datetime = datetime.datetime.strptime(date, '%d%m%Y')
                date_list_str.append(date_datetime)
        except AttributeError:
            date_list_str = None
        try:
            date_from = str(date_list_str[0])
        except IndexError:
            date_from = None
        try:
            date_to = str(date_list_str[1])
        except IndexError:
            date_to = date_from
        return date_from, date_to

    # Define product parse
    def __product_parse(self, tag_product: bs4.Tag) -> dict:
        url = self.start_url
        promo_name = self.get_promo_name(tag_product)
        product_name = self.get_product_name(tag_product)
        old_price = self.get_old_price(tag_product)
        new_price = self.get_new_price(tag_product)
        image_url = self.get_image_url(tag_product)
        date_from, date_to = self.get_data_from(tag_product)
        product = {
            "url": url,
            "promo_name": promo_name,
            "product_name": product_name,
            "old_price": old_price,
            "new_price": new_price,
            "image_url": image_url,
            "date_from": date_from,
            "date_to": date_to,
        }
        return product

    # todo save everything in DB

    # Define the save
    def save(self, product: dict):
        # self.collection.insert_one(product)
        print(product)


# Do the run
if __name__ == '__main__':
    parser = MagnitParse(url, db_client)
    parser.run()
