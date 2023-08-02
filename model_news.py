import requests
from bs4 import BeautifulSoup as bs

from urls_consts import URL_NEWS


def get_top_news() -> dict:
    top_news = {}
    r = requests.get(URL_NEWS)
    soup = bs(r.text, "html.parser")
    top_news_web_components = soup.find_all(class_="material-list__title", limit=6)
    for news in top_news_web_components:
        a_href = news.find("a").get("href")
        top_news.update({news.text.strip(): a_href})
    return top_news
