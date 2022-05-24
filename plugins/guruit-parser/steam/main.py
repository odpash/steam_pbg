import requests
import sys
from bs4 import BeautifulSoup


def main():
    args = sys.argv
    if len(args) != 2:
        return "Вы должны передавать 1 аргумент!"

    url = 'https://store.steampowered.com/app/' + args[1]
    try:
        r = requests.get(url)
        r2 = requests.get(r.url + "?l=russian")
    except:
        return "Connection error!"

    if r.url == 'https://store.steampowered.com/':
        return "Такой страницы не существует!"

    try:
        soup = BeautifulSoup(r.text, features='lxml')
        soup2 = BeautifulSoup(r2.text, features='lxml')
    except:
        return "Unsupported answer"

    try:
        icon_url = soup.find('img', {'class': 'game_header_image_full'})['src']
    except:
        icon_url = ''

    url = r.url

    try:
        year = soup.find('div', {'class': 'date'}).text.strip()
    except:
        year = ''

    try:
        price = soup.find('div', {"class": 'game_purchase_action_bg'}).find('div').get('data-price-final')
    except:
        price = ''

    try:
        desc_eng = soup.find('div', {'id': 'game_area_description'})
    except:
        desc_eng = ''

    try:
        desc_ru = soup2.find('div', {'id': 'game_area_description'})
    except:
        desc_ru = ''

    try:
        title = soup.find('div', {'id': 'appHubAppName'}).text.strip()
    except:
        title = ''
    medias = soup.find('div', {'class': 'highlight_overflow'})
    images = []

    try:
        imgs_all = medias.find_all('a', {'class': 'highlight_screenshot_link'})
        for i in imgs_all:
            images.append(i.get('href'))
    except:
        pass
    video = ''
    videos_all = medias.find_all('div', {'data-panel': '{"focusable":true,"clickOnActivate":true}'})
    for i in videos_all:
        x = i.get('data-mp4-source')
        if video is not None:
            video = x
            break

    try:
        points = soup2.find_all('a', {'class': 'app_tag'})
        for i in range(len(points)):
            points[i] = points[i].text.strip()
    except:
        points = []
    return {'icon_url': icon_url, 'youtube_id': video, 'imgs_en': images, 'title': title, 'tags': points,
            'desc_en': desc_eng, 'desc_ru': desc_ru, 'price': price, 'year': year, 'url': url}


if __name__ == "__main__":
    print(main())
