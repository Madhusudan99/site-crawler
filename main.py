from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json

class JustDailAPI:
    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.site_url = 'https://www.justdial.com/'

    def get_html(self, city, keyword):
        self.city = city
        self.keyword = keyword
        self.generated_url = self.site_url + self.city + '/' + self.keyword
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get(self.generated_url)
        self.page_source = self.driver.page_source
        self.driver.quit()
        return self.page_source

    def get_data(self, page_source):
        self.soup = BeautifulSoup(page_source, 'lxml')
        self.keyword_list = self.soup.find_all("li", class_="cntanr")
        self.data_list_of_dict = []
        for k in self.keyword_list:
            self.data_list_of_dict.append({
                'name': k.find("span", class_="lng_cont_name").get_text(),
                'link': k.find("a")['href'],
                'address': k.find("span", class_="cont_fl_addr").get_text()
            })
        return self.data_list_of_dict


if __name__ == '__main__':
    jd = JustDailAPI()
    page_source = jd.get_html(city='Ahmedabad', keyword='Chemists')
    d = jd.get_data(page_source=page_source)
    print(d)
    with open('/home/defcon/Desktop/ahmedabad.json', 'w') as json_file:
        json.dump(d, json_file, indent=2)