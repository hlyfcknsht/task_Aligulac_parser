from bs4 import BeautifulSoup
import requests
import csv
from PIL import Image
from io import BytesIO
import os
def parsing():
    url = f'http://aligulac.com/periods/latest/?page={1}&sort=&race=ptzrs&nats=all'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
    }

    # Фильтр списка по слову flag в урле картинки
    def filter_flags(img_src):
        flags = [link for link in img_src if 'flag' in link.lower()]
        return flags

    # Обработка списка тегов  img , изъятие чистой ссылки
    def only_src(list):
        img_src = []
        for i in list:
            img_src.append(i['src'])
        return img_src

    # Обработка списка элементов верстки с текстовым содержимым. Изъятие списка содержимого
    def without_text(parsing_data):
        onlyText = [interation.get_text(strip=True) for interation in parsing_data]
        return onlyText


    # Проверка наличия созданной папки, в соотв со значением output_folder
    def checkPath(output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    # Функция для перепостроения списка готовой статистики от вида "В строку" в вид "В столбец"
    def create_new_list(old_list):
        new_list = []
        for i in range(40):
            new_element = []
            for j in range(7):
                if i < len(old_list[j]):
                    new_element.append(old_list[j][i])
                else:
                    new_element.append(None)
            new_list.append(new_element)
        return new_list

    # Запись значений списка в csv файл
    def write_in_csv():
        checkPath('stats')
        with open('stats/statistic_starcraft2.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(list_names)
            for row in data:
                for i in range(num_columns):
                    writer.writerow([row[i]])

    # Парсинг картинок из списка
    def download_images_from_list(image_urls):
        output_folder = 'flags'
        checkPath(output_folder)
        for index, url in enumerate(image_urls):
            response = requests.get(url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                image_filename = f"image_{index}.jpg"
                image.save(os.path.join(output_folder, image_filename))

    page = requests.get(url, headers=headers)
    allPage = BeautifulSoup(page.content, 'html.parser')
    rating_area = allPage.find('table', class_='table table-striped table-hover')
    number = without_text(allPage.find_all('td', class_='rl_number'))
    names = without_text(allPage.find_all('td', class_='rl_name'))
    teams = without_text(allPage.find_all('td', class_='rl_team'))
    all_rating = without_text(allPage.find_all('td', class_='rl_rating'))
    image = rating_area.find_all('img')
    img_src = only_src(image)
    download_images_from_list(filter_flags(img_src))
    rl_rating = all_rating[0:160:4]
    Vp = all_rating[1:160:4]
    Vt = all_rating[2:160:4]
    Vz = all_rating[3:160:4]

    # img_parsing(flags, names)
    all_score_old = [number, names, teams, rl_rating, Vp, Vt, Vz]
    all_score_new = create_new_list(all_score_old)

    num_columns = 40
    data = [all_score_new]
    list_names = ['NUMBER', 'NAMES', 'TEAMS', 'RATING', 'VP', 'VT', 'VZ']
    write_in_csv()


parsing()
