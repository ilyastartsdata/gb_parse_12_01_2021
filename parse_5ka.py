import json
import time
import pathlib import Path
import requests

"""
GET
POST
PUT
PUTCH
DELETE
"""

"""
1xx - Information
2xx - OK
3xx - Redirect
4xx - Client Error
5xx - Server Error
"""

# url = 'https://5ka.ru/api/v2/special_offers/'
# params = {
#    'records_per_page': 100,
#    'page': 1,
# }
#
# headers = {
#    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
#    "Accept-Language": "en-US,en;q=0.5",
# }
#
# response: requests.Response = requests.get(url, params=params, headers=headers)
#
# with open('5ka.ru.html', "w", encoding="UTF-8") as file:
#    file.write(response.text)
#
#
# print(1)

class ParseError(Exception):
    def __init__(self, txt):
        self.txt = txt

class Parse5ka:
    params = {
        'records_per_page': 100,
        'page': 1,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
        "Accept-Language": "en-US,en;q=0.5",
    }

    def __init__(self, start_url, result_path):
        self.start_url = start_url
        self.result_path

    def __get_response(self, url, *args, **kwargs) -> requests.Response:
        while True:
            try:
                response = requests.get(url, *args, **kwargs)
                if response.status_code > 399:
                    raise ParseError(response.status_code)
                time.sleep(0.1)
                return response
            except (requests.RequestException, ParseError):
                time.sleep(0.5)
                continue

    def run(self):
        for product in self.parse(self.start_url):
            self.result_path.joinpath(f"{product['id']}.json")
            self.save(product, path)

    def parse(self, url):
        params = self.params
        while url:
            response = self.__get_response(url, params=params, headers=self.headers)
            if params:
                params = {}
            data = json.loads(response.text)
            url = data.get('next')
            for product in data.get('results'):
                yield product

    @staticmethod
    def save(self, data, path:Path):
        with path.open("w", encoding="UTF-8") as file:
            json.dump(data, file, ensure_ascii=False)
        print(1)

if __name__ == '__main__':
    result_path = Path(__file__).parent.joinpath('products')
    url = 'https://5ka.ru/api/v2/special_offers/'
    parser = Parse5ka(url, result_path)
    parser.run()


