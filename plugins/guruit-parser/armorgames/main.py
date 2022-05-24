import bs4
import requests
from bs4 import BeautifulSoup
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}


def read_config():
    return json.loads(open('config_ag.json').read())['pages_count']


def read_last_id():
    return int(open('last_id.txt').read().strip())


def write_last_id(last_id):
    with open('last_id.txt', 'w') as f:
        f.write(str(last_id))
    f.close()


def main():
    ans = []
    pages_count = read_config()
    last_id = read_last_id()

    for _ in range(pages_count):
        description_rus = ''
        description_eng = ''
        last_id += 1
        while True:
            url = f'https://armorgames.com/symbiosis-game/{last_id}?fp=ng'
            r = requests.get(url, headers=headers)
            if 'Page Not Found' in r.text or 'is currently not available on Armor Games' in r.text:
                last_id += 1
            else:
                break
        soup = BeautifulSoup(r.text, features='lxml')

        images = []
        try:
            buff = r.text.split('http://cache.armorgames.com/files/fileimages/')[1::]
            for i in buff:
                images.append('http://cache.armorgames.com/files/fileimages/' + i.split('"')[0])
        except:
            pass

        try:
            tags = soup.find('div', {'class': 'tags'}).find_all('a', {'class': 'tag-category'})
            for i in range(len(tags)):
                tags[i] = tags[i].text.strip()
        except:
            tags = []

        try:
            name = soup.find('h1').text.strip()
        except:
            name = ''
        date = ''
        try:
            description_tab = soup.find('div', {'id': 'description-tab'})

            try:
                published_table = description_tab.find('table', {'class': 'stats'}).find_all('td')
            except:
                published_table = []
            for i in published_table:
                try:
                    i = i.find_all('div')
                    if 'Published' in i[0].text:
                        date = i[1].text.strip()
                except:
                    pass
            description_eng = description_tab.find('article', {'id': 'description'})
            description_rus = ''
        except:
            pass
        icon = f'https://gamemedia.armorgames.com/{last_id}/icn_thmb.png'
        price = ''
        ans.append({'icon_url': icon, 'youtube_id': '', 'imgs_en': images, 'title': name, 'tags': tags,
                    'desc_en': description_eng, 'desc_ru': description_rus, 'price': price, 'year': date, 'url': url})
    write_last_id(last_id)
    return ans


if __name__ == "__main__":
    print(main())
