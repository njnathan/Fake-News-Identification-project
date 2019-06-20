import requests
from bs4 import BeautifulSoup
import pymysql

links = []
fake_text = []


def get_snopes_links(root_url):

    while True:
        print('scanning ' + root_url)
        r = requests.get(root_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        for data in soup.find_all('div', class_='list-group'):
            for a in data.find_all('a'):
                links.append(a.get('href'))

        next_page = soup.find("div", class_="card-footer pagination btn-group")

        if next_page:
            next_url = next_page.find("a", class_="btn-next btn btn-outline-primary", href=True)
            if next_url:
                root_url = next_url['href']
            else:
                break
        else:
            break


def get_fake_article_text(links):
    for link in links:
        combQuote = ""
        quote = ""
        print('scanning ' + link)
        root_url = link
        r = requests.get(root_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        for data in soup.find_all('blockquote', class_=''):

            quote = data.text
            combQuote = combQuote + " " + quote
        if combQuote != "":
            fake_text.append(combQuote)



def submit_fake_articles(fake_text):
    db = pymysql.connect(host="localhost", user='ylb14192', password='201445765', database='ylb14192')
    cursor = db.cursor()
    for i in range(0, 1000):
        text = fake_text[i]
        insertCommand = "INSERT INTO `train`(`id`, `article-text`, `authentic`) VALUES (%s, %s, %s)"
        cursor.execute(insertCommand, (None, text, 0))
        db.commit()
    db.close()

    db2 = pymysql.connect(host="localhost", user='ylb14192', password='201445765', database='ylb14192')
    cursor2 = db2.cursor()
    for i in range(1001, 1501):
        text = fake_text[i]
        insertCommand = "INSERT INTO `test`(`id`, `article-text`, `authentic`) VALUES (%s, %s, %s)"
        cursor2.execute(insertCommand, (None, text, 0))
        db2.commit()
    db2.close()

get_snopes_links('https://www.snopes.com/fact-check/category/junk-news/')
get_snopes_links('https://www.snopes.com/tag/fake-news/')
get_fake_article_text(links)
submit_fake_articles(fake_text)





