import requests
import bs4
from fake_useragent import UserAgent
from datetime import datetime
import re

# определяем список ключевых слов
KEYWORDS = ["дизайн", "фото", "web", "python"]

ua = UserAgent()

HEADER = {
    "Accept": "*/*",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": ua.firefox
}

main_url = "https://habr.com/ru/all/"


def get_matching_article(url, words, switch=True):
    response = requests.get(url, headers=HEADER)
    text = response.text
    base_url = re.search(r"https://\w+\.\w+", url)[0]
    soup = bs4.BeautifulSoup(text, features="html.parser")
    articles = soup.find_all("article")
    data_list = []
    for article in articles:
        # TODO: Сбор данных из превью
        title = article.find("h2").find("span").text
        hubs = article.find_all(class_="tm-article-snippet__hubs-item")
        hubs = [hub.find("a").find("span").text for hub in hubs]
        link = base_url + article.find(class_="tm-article-snippet__title-link").attrs["href"]
        article_preview = article.find(class_="tm-article-body tm-article-snippet__lead").find(
            class_="article-formatted-body").text
        article_date = datetime.strptime(article.find("time").attrs["title"], '%Y-%m-%d, %H:%M')

        if switch:
            for word in words:
                word = word.lower()
                if (word in title.lower()) or (word in [hub.lower() for hub in hubs]) or (
                        word in article_preview.lower()):
                    data_list.append(f"{article_date.strftime('%d.%m.%Y %H:%M')} - {title} - {link}")
                    print(f"{article_date.strftime('%d.%m.%Y %H:%M')} - {title} - {link}")
                    break
        else:
            # TODO: Сбор данных из полной статьи
            response_whole_article = requests.get(link, headers=HEADER)
            text2 = response_whole_article.text
            soup2 = bs4.BeautifulSoup(text2, features="html.parser")
            whole_article = soup2.find(class_="tm-article-body").text
            for word in words:
                word = word.lower()
                if (word in title.lower()) or (word in [hub.lower() for hub in hubs]) or (
                        word in whole_article.lower()):
                    data_list.append(f"{article_date.strftime('%d.%m.%Y %H:%M')} - {title} - {link}")
                    print(f"{article_date.strftime('%d.%m.%Y %H:%M')} - {title} - {link}")
                    break
    return data_list


if __name__ == "__main__":
    # Сменив switch параметр функции на False, можно запустить поиск по всей статье (По умолчанию этот параметр True)
    data = get_matching_article(main_url, KEYWORDS)

    with open("result.txt", "wt", encoding="utf-8") as f:
        for i in data:
            f.writelines(i+"\n")
