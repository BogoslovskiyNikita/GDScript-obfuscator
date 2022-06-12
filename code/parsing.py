import csv
import requests
from bs4 import BeautifulSoup

classes_list_url = 'https://docs.godotengine.org/ru/stable/classes/index.html'
classes_base_url = 'https://docs.godotengine.org/ru/stable/classes/'
substring = 'https://docs.godotengine.org/ru/stable/classes/class_'


def get_classes_urls():
    response = requests.get(classes_list_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = soup.find_all('a', class_='reference internal')
    result = []
    for a in urls:
        to_check = classes_base_url + a['href']
        if substring in to_check:
            result.append(to_check)
    return result


def get_properties_and_methods(url):
    result = set()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = soup.find_all('span', class_='std std-ref')
    for url in urls:
        result.add(url.text)
    return result


def get_class_names():
    result = set()
    response = requests.get(classes_list_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = soup.find_all('a', class_='reference internal')
    for url in urls:
        to_check = classes_base_url + url['href']
        if substring in to_check:
            result.add(url.text)
    return result


def get_all_properties_and_methods():
    result = set()
    progress = 0
    urls = get_classes_urls()
    for url in urls:
        percent = round(100 * float(progress) / float(len(urls)), 2)
        print(url, ' ', progress, '/', len(urls), ' ', percent, '%', sep='')
        progress += 1
        result.update(get_properties_and_methods(url))
        # print(get_properties_and_methods(url))
    print('\n'.join(result))
    write_set_to_csv(result)
    return result


def write_set_to_csv(s):
    with open('keywords.csv', "w", newline='') as f:
        writer = csv.writer(f)
        rows = zip(list(s))
        for row in rows:
            writer.writerow(row)


def read_set_from_csv():
    with open('keywords.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return [el[0] for el in list(reader)]


