"""
Данные о вакансии:
    - Название вакансии
    - Оклад (строкой от до или просто сумма)
    - Описание вакансии
    - Ключевые навыки - в виде списка названий
    - Ссылка на автора вакансии
"""

# Import the libraries
import scrapy


# Define class for items in vacancy profile
class VacancyItem(scrapy.Item):
    _id = scrapy.Field()
    vac_name = scrapy.Field()
    salary = scrapy.Field()
    vac_info = scrapy.Field()
    key_skills = scrapy.Field()
    employer_url = scrapy.Field()


"""
Данные о работодателе:
    - Название
    - Сайт ссылка (если есть)
    - Сферы деятельность (списком)
    - Описание
"""


# Define class for items in employer profile
class EmployerItem(scrapy.Item):
    _id = scrapy.Field()
    emp_name = scrapy.Field()
    url = scrapy.Field()
    area_of_activity = scrapy.Field()
    emp_description = scrapy.Field()
    emp_vacancy_offer = scrapy.Field()
