import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import xlrd
import re

#Parsing of site https://bashesk.ru/corporate/tariffs/unregulated/limits/
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

# parsing of files
book = xlrd.open_workbook('files/1.xls')
sheet = book.sheet_by_name('1 ц.к. ')
# print(book.sheet_names())
pattern = r"^text:\'г) объем фактического пикового потребления гарантирующего поставщика на оптовом рынке, МВт   \'$"
for row in sheet.get_rows():
    print(row) #нужно как-то вычленить 'number:'
