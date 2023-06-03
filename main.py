'''
Попробуем получать интересующие вакансии на сайте headhunter самыми первыми :)

Необходимо парсить страницу со свежими вакансиями с поиском по "Python" и городами "Москва" и "Санкт-Петербург". Эти параметры задаются по ссылке
Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".
Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.
Получать вакансии только с ЗП в долларах(USD)
'''

import requests
import re
from fake_headers import Headers
import bs4
import json

link = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers = Headers(browser='firefox', os='win')
headers_data = headers.generate()

main_page_html = requests.get(link, headers=headers_data).text
main_page_soup = bs4.BeautifulSoup(main_page_html, 'lxml')

div_vacancy_list_tag = main_page_soup.find('div', id='a11y-main-content')
vacancy_tags = div_vacancy_list_tag.find_all('div', class_='serp-item')

vacancy_list = []

for vacancy_tag in vacancy_tags:   
    django = False
    flask = False
    salary_tag = vacancy_tag.find(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
    if salary_tag:
        salary = salary_tag.text
    if re.search('[USDusd]', salary):
    # if re.search('[.]', salary):

        company_name_tag = vacancy_tag.find(attrs={'data-qa': 'vacancy-serp__vacancy-employer'})
        if company_name_tag:
            company_name_text = company_name_tag.text
            company_name = company_name_text.split(',')[0]
        company_address_tag = vacancy_tag.find(attrs={'data-qa': 'vacancy-serp__vacancy-address'})
        if company_address_tag:
            company_address = company_address_tag.text
            company_city = company_address.split(',')[0]
            
        a_tag = vacancy_tag.find("a")
        vacancy_link = a_tag["href"]
        full_vacancy_html = requests.get(vacancy_link, headers=headers.generate()).text
        full_vacancy_soup = bs4.BeautifulSoup(full_vacancy_html, features="lxml")

        vacancy_skills_tags = full_vacancy_soup.find_all("div", class_="bloko-tag bloko-tag_inline")
        for vacancy_skills_tag in vacancy_skills_tags:                  
            vacancy_skills_text = vacancy_skills_tag.text
            if (vacancy_skills_text.lower()).find('django') >= 0:
                django = True
            if (vacancy_skills_text.lower()).find('Flask') >= 0:
                flask = True
        
        vacancy_description_tag = full_vacancy_soup.find("div", class_="vacancy-description")
        vacancy_user_content_tag = full_vacancy_soup.find("div", class_="g-user-content")
        user_content_parts = vacancy_user_content_tag.find_all('p')
        for part in user_content_parts:
            part_text = part.text
            if (part_text.lower()).find('django') >= 0:
                django = True
            if (part_text.lower()).find('flask') >= 0:
                flask = True  

        if django and flask:
        # if django or flask:
            vacancy = {
                "link": vacancy_link,
                "salary": salary,
                "company_name": company_name,
                "city": company_city,
            }
            vacancy_list.append(vacancy)
            
with open('result.json', 'w') as f:
    json.dump(vacancy_list, f, ensure_ascii=False)
            
 




