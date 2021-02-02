# Homework 5

"""
Task:

Source: https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113

Вакансии удаленной работы
Задача:

    Обойти с точки входа все вакансии и собрать след данные:
        1. Название вакансии
        2. Оклад (строкой от до или просто сумма)
        3. Описание вакансии
        4. Ключевые навыки - в виде списка названий
        5. Ссылка на автора вакансии

    Перейти на страницу автора вакансии, собрать данные:
     1. Название
     2. Сайт ссылка (если есть)
     3. Сферы деятельности (списком)
     4. Описание

Обойти и собрать все вакансии данного автора.
Обязательно использовать Loader Items Pipelines
"""

# Import the necessary libraries
import scrapy
from ..loaders import VacancyLoader, EmployerLoader


# Define the class to grab the data
class TltHhSpider(scrapy.Spider):

    name = 'tlt_hh'
    allowed_domains = ['togliatti.hh.ru']
    start_urls = ['https://togliatti.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    xpath = {
        'vacancy_urls': '//a[@data-qa="vacancy-serp__vacancy-title"]/@href',
        'pagination': '//div[@data-qa="pager-block"]//a[@data-qa="pager-page"]/@href'
    }

    vacancy_xpath = {
        'vac_name': '//h1[@data-qa="vacancy-title"]/text()',
        'salary': '//p[@class="vacancy-salary"]/span[@data-qa="bloko-header-2"]//text()',
        'vac_info': '//div[@data-qa="vacancy-description"]//text()',
        'key_skills': '//div[@class="bloko-tag-list"]//span[@data-qa="bloko-tag__text"]//text()',
        'employer_url': '//a[@data-qa="vacancy-company-name"]/@href',
    }

    employer_xpath = {
        'emp_name': '//span[@data-qa="company-header-title-name"]/text()',
        'url': '',
        'area_of_activity': '//div[@class="employer-sidebar-content"]//div[@class="employer-sidebar-block__header"]/text()',
        'emp_description': '//div[@class="g-user-content"]//text()',
    }

    employer_vacancies_list = []

    # Define parse
    def parse(self, response):
        pages = response.xpath(self.xpath['pagination'])
        for page in pages:
            yield response.follow(page, callback=self.parse)
        vacancies = response.xpath(self.xpath['vacancy_urls'])
        for vac_url in vacancies:
            yield response.follow(vac_url, callback=self.vacancy_parse)

    # Define parser for vacancy
    def vacancy_parse(self, response):
        loader = loaders.VacancyLoader(response=response)
        for key, val in self.vacancy_xpath.items():
            loader.add_xpath(key, val)
        yield loader.load_item()

        emp_url_path = response.xpath(self.vacancy_xpath['employer_url']).get()
        yield response.follow(emp_url_path, callback=self.company_parse)

    # Define parser for company
    def company_parse(self, response):
        loader = loaders.EmployerLoader(response=response)
        for key, val in self.employer_xpath.items():
            if key == 'url':
                loader.add_value(key, response.url)
            else:
                loader.add_xpath(key, val)

        # Bypass and collect all the jobs of this author
        emp_vacancy_path = response.xpath('//a[@data-qa="employer-page__employer-vacancies-link"]/@href').get()
        yield response.follow(emp_vacancy_path, callback=self.__get_company_vacancies_urls)
        loader.add_value('emp_vacancy_offer', self.employer_vacancies_list)
        yield loader.load_item()

    # Define the vacancies' urls for company
    def __get_company_vacancies_urls(self, response):
        self.employer_vacancies_list = response.xpath(
            '//div[@class="vacancy-serp"]//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
