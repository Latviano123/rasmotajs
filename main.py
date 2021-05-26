from bs4 import BeautifulSoup
import requests
import csv

url = 'https://data.gov.lv/dati/lv/dataset'

def getdata(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup

def getnextpage(soup):
    page = soup.find('ul', class_='pagination')
    try:
        if '»' in page.text:
            links = page.find_all('a')
            for link in links:
                if '»' in link.text:
                    url = 'https://data.gov.lv' + str(link.get('href'))
            return url
        else:
            return
    except:
        if page not in soup:
            pass


csv_file = open('scrape.csv', 'w', newline='', encoding="utf-8")

csv_writer = csv.writer(csv_file, delimiter=';')
csv_writer.writerow(['Headline', 'Summary', 'Organization', 'Category', 'File format', 'Views', 'Tags', 'URL'])

while True:
    soup = getdata(url)
    url = getnextpage(soup)
    for article in soup.find_all('li',class_='dataset-item'):

        urls = 'https://data.gov.lv' + str(article.h3.a.get('href'))
        print(urls)

        r_urls = requests.get(urls).text
        zupa = BeautifulSoup(r_urls, 'lxml')

        try:
            headline = zupa.find('h1', class_='heading').text
            print(headline)
        except:
            headline = None
            headline1 = article.h3.a.text
            print(headline1)

        try:
            summary = zupa.find('div', class_='notes').text.strip()
            print(summary)
        except:
            summary = None
            summary1 = article.find('div', class_='dataset-content').div.text
            print(summary1)

        try:
            organization = zupa.find('section', class_='module-content').h1.text.strip()
            print(organization)
        except:
            organization = None

        col = article.find('div', class_='col-sm-3')
        span_tag = col.select('span')

        try:
            categ = zupa.find(lambda tag: tag.name == 'a' and ('Groups' in tag.text or 'Kategorijas' in tag.text))
            cat = 'https://data.gov.lv' + str(categ.get('href'))
            r_cat = requests.get(cat).text
            zupa_cat = BeautifulSoup(r_cat, 'lxml')

            j = 0
            category = ''
            categ = zupa_cat.find('ul', class_='media-grid')
            for cat_h3 in categ.find_all('h3'):
                category += cat_h3.text + ', '
                j += 1
                if j == len(categ.find_all('h3')): print(category, end='\n')
        except:
            category = span_tag[0].text.strip()
            print(category)

        try:
            i = 0
            forma = ''
            col_ul = col.find('ul', class_='dataset-resources')
            for col_li in col_ul.find_all('li'):
                forma += col_li.a.text + ', '
                i += 1
                if i == len(col_ul.find_all('li')): print(forma, end='\n')
        except:
            form = None

        try:
            k = 0
            tag = ''
            sec_tag = zupa.find('ul', class_='tag-list')
            for tag_li in sec_tag.find_all('li'):
                tag += tag_li.a.text + ', '
                k += 1
                if k == len(sec_tag.find_all('li')): print(tag, end='\n')
        except:
            tag = None

        views = span_tag[1].text.strip()
        print(views)

        print()

        csv_writer.writerow([headline or headline1, summary or summary1, organization, category, forma, views, tag, urls])

    if not url:
        break

csv_file.close()