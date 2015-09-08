from bs4 import BeautifulSoup
import requests
import re
import os

URL = 'http://www.artsandscience.utoronto.ca/ofr/timetable/winter/'


def store_html_page(name, body):
    f = open(os.path.dirname(__file__) + '/html_data/' + name, 'w')
    f.write(body.encode('utf-8'))
    f.close()


def store_html_data():
    req = requests.get(URL)
    f = open(os.path.dirname(__file__) + '/html_data/links.txt', 'w')
    if req.status_code != 200:
        return False

    regex = re.compile('^\w*.html$')
    body = BeautifulSoup(req.text, 'html.parser')
    links = body.find('li').findAll('a')

    for link in links:
        html_link = str(link.get('href'))
        matched = regex.match(html_link)
        if not matched:
            continue
        f.write(html_link + '\n')
        html_data = requests.get(URL + html_link)
        if html_data.status_code == 200:
            store_html_page(html_link, html_data.text)
    f.close()




