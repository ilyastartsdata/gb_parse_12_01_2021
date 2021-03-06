# Import the necessary libraries
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader
from scrapy import Selector

from items import VacancyItem, EmployerItem

# Define the class to load the vacancies
class VacancyLoader(ItemLoader):
    default_item_class = VacancyItem
    vac_name_out = TakeFirst()
    salary_out = ''.join
    vac_info_in = ''.join
    vac_info_out = TakeFirst()
    employer_url_out = TakeFirst()

# Define the class to load the employer
class EmployerLoader(ItemLoader):
    default_item_class = EmployerItem
    emp_name_out = TakeFirst()
    url_out = TakeFirst()
    area_of_activity_out = TakeFirst()
    emp_description_in = ''.join
    emp_description_out = TakeFirst()