import requests
from bs4 import BeautifulSoup

def g(url):
    # try:
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    r = requests.get(url, headers=header, timeout=30)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup)
    x = soup.find_all(class_='main-content')
    print(x)

g('https://news.sina.com.cn/china/')