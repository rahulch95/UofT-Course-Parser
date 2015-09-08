from bs4 import BeautifulSoup
import requests
import re
import os

TIMETABLE_URL = 'http://www.artsandscience.utoronto.ca/ofr/timetable/winter/'
HTML_DATA_DIR = os.path.dirname(__file__) + '/html_data/'
COURSE_FINDER_URL = 'http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&' \
                    'viewId=CourseDetails-InquiryView&courseId='
COURSE_FINDER_MAPPING = {
    'Y': '20159',
    'F': '20159',
    'S': '20161'
}

def store_html_page(name, body):
    f = open(HTML_DATA_DIR + name, 'w')
    f.write(body.encode('utf-8'))
    f.close()


def store_html_data():
    req = requests.get(TIMETABLE_URL)
    f = open(HTML_DATA_DIR + 'links.txt', 'w')
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
        html_data = requests.get(TIMETABLE_URL + html_link)
        if html_data.status_code == 200:
            store_html_page(html_link, html_data.text)
    f.close()
    return True


def get_course_finder_data(course_code, course_term):
    url = COURSE_FINDER_URL + course_code + str(COURSE_FINDER_MAPPING[course_term])
    body = requests.get(url)
    if body.status_code != 200:
        return False

    html_body = BeautifulSoup(body.text, 'html.parse')
    table = html_body.find('table')
    tableData = [[col.get_text().encode('utf-8').replace('\n', '').replace('\r', '').strip() for col in row.findAll("td")] for row in table.findAll("tr")]
    # store table data in proper format into course finder


def parse_and_store_courses():
    files = os.listdir(HTML_DATA_DIR)
    for file in files:
        if file == 'links.txt':
            continue
        f = open(HTML_DATA_DIR + file, 'r')
        body = BeautifulSoup(f.read(), 'html.parser')
        f.close()
        table = body.find('table')
        tableData = [[col.get_text().encode('utf-8') for col in row.findAll("td")] for row in table.findAll("tr")]
        regex = re.compile('\w{3}\d{3}\w\d')
        for row in tableData:
            if len(row) and regex.match(row[0]):
                course_code = row[0] + row[1]
                course_term = row[1]
                course_name = row[2]
                get_course_finder_data(course_code, course_term)
