import requests
from bs4 import BeautifulSoup

file_number = 1
link = f'https://bashesk.ru/corporate/tariffs/unregulated/limits/'
params = {
    'filter_name': 'Предельные уровни нерегулируемых цен на электрическую энергию (мощность), поставляемую потребителям (покупателям) ООО "ЭСКБ", (с максимальной мощностью энергопринимающих устройств до 670 кВт)',
    'filter_date_from': '01.07.2019',
    'filter_date_to': '01.07.2020'
}

res = requests.get(link, params=params).text
soup = BeautifulSoup(res, 'lxml')
all_files = soup.find_all('div', 'col-2')

for file in all_files:
    file_link = file.find('a').get('href')
    download_file = requests.get(f'https://bashesk.ru/{file_link}').content

    with open(f'files/{file_number}.xls', 'wb') as dw_file:
        dw_file.write(download_file)

    file_number += 1

