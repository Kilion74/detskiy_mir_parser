import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4
import random
import time
import csv

# pip install lxml


# Список пользовательских агентов
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/112.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177',
    'Mozilla/5.0 (Linux; Android 11; Pixel 4 XL Build/RQ3A.210705.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36'
]


# Функция для получения случайного пользовательского агента
def get_random_user_agent():
    return random.choice(user_agents)


url = 'https://www.detmir.ru/catalog/index/name/myagkie_igrushki/'
headers = {
    'User-Agent': get_random_user_agent(),
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'  # Исправлено здесь
}
data = requests.get(url, headers=headers).text
time.sleep(2)
block = BeautifulSoup(data, 'lxml')
heads = block.find('div', id=':Rmarnjd:').find_all('section')
print(len(heads))
for head in heads:
    link = head.find('a')['href']
    print(link)
    loop = requests.get(link, headers=headers).text
    time.sleep(1)
    stock = BeautifulSoup(loop, 'lxml')
    name = stock.find('h1').text.strip()
    print(name)
    try:
        price = stock.find('p', class_='bsX bsZ').text.strip()
        print(price)
    except:
        price = stock.find('p', class_='bsX').text.strip()
        print(price)
    try:
        discription = stock.find('div', class_='uS uW').find('p').text.strip()
        print(discription)
    except:
        discription = stock.find('div', class_='uS uW').text.strip()
        print(discription)
    params = stock.find('table', class_='_X').find_all('tr')
    print(len(params))
    # for param in params:
    #     get_key = param.find_all('th')
    #     get_value = param.find_all('td')

    result = []

    for param in params:
        get_key = param.find_all('th')  # Извлечение заголовков
        get_value = param.find_all('td')  # Извлечение значений

        # Параметр result будет содержать строку с конкатенированными значениями
        for key, value in zip(get_key, get_value):
            # Извлекаем текст из заголовка и значения, убирая пробелы
            key_text = key.get_text(strip=True)
            value_text = value.get_text(strip=True)

            # Конкатенируем ключ и значение
            combined_text = f"{key_text}: {value_text}"
            result.append(combined_text)


    # Вывод результата
    get_param = []
    for item in result:
        print(item)
        get_param.append(item)

    photoes = stock.find('div', class_='CB').find_all('source')
    print(len(photoes))
    get_pix = []
    for item in photoes:
        print(item.get('srcset').replace('3x', ' '))
        get_pix.append(item.get('srcset').replace('3x', ' '))
    print('\n')

    storage = {'name': name, 'price': price, 'discription': discription, 'params': '; '.join(get_param),
               'foto': '; '.join(get_pix)}
    fields = ['Name', 'Price', 'Discription', 'Params', 'Photo']
    with open('storage_2.csv', 'a+', encoding='utf-16') as f:
        pisar = csv.writer(f, delimiter='$', lineterminator='\r')
        # Проверяем, находится ли файл в начале и пуст ли
        f.seek(0)
        if len(f.read()) == 0:
            pisar.writerow(fields)  # Записываем заголовки, только если файл пуст
        pisar.writerow([storage['name'], storage['price'], storage['discription'], storage['params'], storage['foto']])
