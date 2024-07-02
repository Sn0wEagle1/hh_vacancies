import requests
from bs4 import BeautifulSoup
import psycopg2

# URL для поиска вакансий по IT
URL = 'https://hh.ru/search/vacancy'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}
PARAMS = {
    'text': 'программист',  # Можно изменить на другие ключевые слова
    'area': '113',  # Москва
    'page': '0'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r.text


def remove_duplicates(text):
    parts = text.split(',')
    seen = set()
    unique_parts = []
    for part in parts:
        part = part.strip()
        if part not in seen:
            seen.add(part)
            unique_parts.append(part)
    return ', '.join(unique_parts)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y font-inter')

    jobs = []
    for item in items:
        title = item.find('a', class_='bloko-link').text
        link = item.find('a', class_='bloko-link').get('href')
        if not link.startswith('https://hh.ru') and not link.startswith('https://adsrv'):
            link = 'https://hh.ru' + link[link.find('.ru') + 3:]
        company = item.find('span', class_='company-info-text--vgvZouLtf8jwBmaD1xgp').text if item.find('span',
                                                                                                        class_='company-info-text--vgvZouLtf8jwBmaD1xgp') else 'Не указано'
        salary = item.find('span',
                           class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh').text if item.find(
            'span',
            class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh') else 'Не указана'
        vacancy_html = get_html(link)
        vacancy_soup = BeautifulSoup(vacancy_html, 'html.parser')
        skill_blocks = vacancy_soup.find_all('div', class_='magritte-tag__label___YHV-o_3-0-0')
        skills = ', '.join([skill.text.strip() for skill in skill_blocks]) if skill_blocks else 'Не указано'
        raw_address = vacancy_soup.find('span', attrs={'data-qa': 'vacancy-view-raw-address'}).get_text(
            strip=True) if vacancy_soup.find('span', attrs={'data-qa': 'vacancy-view-raw-address'}) else 'Не указано'

        # Обрабатываем каждую часть адреса, добавляя "метро" перед станцией метро
        address_parts = raw_address.split(',')
        processed_parts = []
        metro_stations_text = []
        for part in address_parts:
            part = part.strip()
            metro_station = vacancy_soup.find_all('span', class_='metro-station')
            for station in metro_station:
                station_text = station.get_text(strip=True)
                metro_stations_text.append(station_text)
            if metro_station and part in metro_stations_text:
                processed_parts.append('метро ' + part)
            else:
                processed_parts.append(part)

        metro = ', '.join(processed_parts)
        print(metro)
        metro = remove_duplicates(metro)
        experience = item.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-work-experience'}).get_text(
            strip=True) if item.find('span',
                                     attrs={'data-qa': 'vacancy-serp__vacancy-work-experience'}) else 'Не указано'

        # Удаляем слово "опыт" из строки опыта
        experience = experience.replace('Опыт ', '')

        remote = item.find('span', attrs={'data-qa': 'vacancy-label-remote-work-schedule'}).get_text(
            strip=True) if item.find('span', attrs={'data-qa': 'vacancy-label-remote-work-schedule'}) else 'Не указано'

        jobs.append({
            'title': title,
            'link': link,
            'company': company,
            'salary': salary,
            'skills': skills,
            'metro': metro,
            'experience': experience,
            'remote': remote
        })
    return jobs


def save_to_db(jobs):
    conn = psycopg2.connect(
        dbname='vacancies',
        user='postgres',
        password='Hfnfneq2005',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs_job (
        id SERIAL PRIMARY KEY,
        title TEXT,
        link TEXT,
        company TEXT,
        salary TEXT,
        skills TEXT,
        metro TEXT,
        experience TEXT,
        remote TEXT
    )
    ''')

    for job in jobs:
        cursor.execute('''
        INSERT INTO jobs_job (title, link, company, salary, skills, metro, experience, remote) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (job['title'], job['link'], job['company'], job['salary'], job['skills'], job['metro'], job['experience'],
              job['remote']))

    conn.commit()
    cursor.close()
    conn.close()


def parse():
    jobs = []
    page = 0
    while True:
        PARAMS['page'] = page
        html = get_html(URL, PARAMS)
        if html:
            new_jobs = get_content(html)
            if not new_jobs:
                break
            jobs.extend(new_jobs)
            page += 1
            print(page)
        else:
            break
    return jobs


# Сохранение найденных вакансий в базу данных
jobs = parse()
if jobs:
    save_to_db(jobs)
