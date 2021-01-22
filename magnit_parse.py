import bs4
import lxml as lxml
import requests
from urllib.parse import urljoin
import pymongo


class MagnitParser:

    def __init__(self, start_url, data_base):
        self.start_url = start_url

    @staticmethod
    def __get_response(url, *args, **kwargs):
        # todo обработать ошибки запросов и статусов тут
        response = requests.get(url, *args, **kwargs)
        return response

    @property
    def data_template(self):
        return {
            "url": lambda tag: urljoin(self.start_url, tag.attrs.get("href")),
            "title": lambda tag: tag.find("div", attrs={"class": "card-sale__title"}).text,
        }

    @staticmethod
    def __get_soup(response):
        return bs4.BeautifulSoup(response.text, "lxml")

    def run(self):
        for product in self.parse(self.start_url):
            self.save(product)

    def validate_product(self, product_data):
        return product_data

    def parse(self, url):
        soup = self.__get_soup(self.__get_response(url))
        catalog_main = soup.find('div', attrs={"class": "catalogue__main"})
        for product_tag in catalog_main.find_all("a", attrs={"class": "card-sale"}, reversive=False):
            yield self.__get_product_data(product_tag)

    def __get_product_data(self, product_tag):
        data = {}
        for key, pattern in self.data_template.items():
            try:
                data[key] = pattern(product_tag)
            except AttributeError:
                continue
        return data

    def save(self, data):
        print(data)


if __name__ == '__main__':
    data_base = pymongo.MongoClient("mongodb://localhost:27017")
    parser = MagnitParser("https://magnit.ru/promo/?geo=moskva")
    parser.run()
