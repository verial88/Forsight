import requests
from bs4 import BeautifulSoup
import xlrd
import os

# Парсинг сайта https://bashesk.ru/corporate/tariffs/unregulated/limits/
if not 'downloads' in os.listdir():
    os.mkdir('downloads') # создаем директорию для скачивания файлов

# создаем параметры для get-запроса (url + params)
link = f'https://bashesk.ru/corporate/tariffs/unregulated/limits/'
params = {
    'filter_name': 'Предельные уровни нерегулируемых цен на электрическую энергию (мощность), поставляемую потребителям (покупателям) ООО "ЭСКБ", (с максимальной мощностью энергопринимающих устройств до 670 кВт)',
    'filter_date_from': '01.07.2019',
    'filter_date_to': '01.07.2020'
}
# с помощью библиотек requests и BeautifulSoup делаем запрос к сайту и ищем все ссылки на нужные нам файлы (по структуре сайта
# они находятся в тегах div и классах col-2
res = requests.get(link, params=params).text
soup = BeautifulSoup(res, 'lxml')
all_files = soup.find_all('div', 'col-2')
# нужные нам ссылки имеют тег a и параметр href
for file in all_files:
    file_link = file.find('a').get('href')
    file_name = file_link.split('/')
    download_file = requests.get(f'https://bashesk.ru/{file_link}').content # скачиваем файлы
# Записываем скачанные файлы в папку files
    with open(f'downloads/{file_name[-1]}', 'wb') as dw_file:
        dw_file.write(download_file)

# Парсинг файлов

for file_pars in os.listdir('downloads'):
    book = xlrd.open_workbook(f'downloads/{file_pars}')
    sheet = book.sheet_by_name('1 ц.к. ')

    for row in sheet.get_rows():
        if 'г) объем фактического пикового потребления гарантирующего поставщика на оптовом рынке, МВт' in row[0].value:
            print(f'Значение из файла {file_pars}: ', row[15].value)
            break
