import requests
from bs4 import BeautifulSoup

def parse_news():
    url = 'https://library.bsuir.by'
    news_list = []
    response = requests.get(url)
    bs = BeautifulSoup(response.content, 'html.parser')
    for link in bs.find('div', 'm_g_slides').find_all('a'):
        sub_url = url + link.get("href")
        sub_bs = BeautifulSoup(requests.get(url=sub_url).content, 'html.parser')
        news_list.append({
            'title': f'{sub_bs.find("div", "info-page-container").find("h1").text}',
            'img': f'{url + sub_bs.find("div", "info-page-container").find("img").get("src")}',
            'news_url': f'{url}{link.get("href")}'
        })

    return news_list