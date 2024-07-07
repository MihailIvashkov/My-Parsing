from selenium import webdriver
from time import sleep
from datetime import datetime as dt
import csv
import bs4
def percent(total_sum, name_capitalization) -> dict:
    """Функция вычисляет процент капитализации криптовалюты от общей суммы капитализации криптовалют"""
    name_capitalization_percent = {}
    for name, capitalization_str in name_capitalization.items():
        capitalization_int = int(''.join(filter(str.isdigit, capitalization_str)))
        percent = int(capitalization_int / total_sum * 100)
        name_capitalization_percent[name] = {"capitalization": capitalization_str[1:], "percent": f"{percent}%"}
    return name_capitalization_percent


def save(data):
    """Функция записывает данные в CSV файл"""
    name_file = dt.now().strftime('%H.%M %d.%m.%Y')
    with open(f'{name_file}.csv', 'w', encoding='UTF-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')
        writer.writerow(('Name', 'MC', 'MP'))
        for name, cap_per in data.items():
            writer.writerow((name, cap_per['capitalization'], cap_per['percent']))


def parser() -> dict:
    """Парсинг сайт coinmarketcap.com. Выборка данных(наименование, капитализация) 100 криптовалют"""
    driver = webdriver.Chrome()
    driver.get('https://coinmarketcap.com/')
    driver.maximize_window()
    px = 0
    for i in range(10):
        px += 1000
        driver.execute_script(f'window.scrollTo(0, {px})')
        sleep(0.1)
    html = driver.page_source
    driver.close()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find('tbody').find_all('tr')
    name_capitalization = {}
    for tr in table:
        try:
            all_td = list(tr.find_all('td'))
            name = all_td[2]
            name = name.find_all('p')[0].get_text()
            capitalization = all_td[7]
            capitalization = capitalization.find_all('span')[1].get_text()
            name_capitalization[name] = capitalization
        except IndexError as e:
            print(e)
    return name_capitalization


def total_sum(data) -> int:
    sum = 0
    for key, value in data.items():
        sum += int(''.join(filter(str.isdigit, value)))
    return sum


name_capitalization = parser()
print('Парсинг завершён')
total_sum = total_sum(name_capitalization)
print(f'Общая сумма капитализации: {total_sum}$')
name_capitalization_percent = percent(total_sum, name_capitalization)
print('Обработка данных завершена')
save(name_capitalization_percent)
print('Файл CSV сохранён')
print('Все задачи завершены')