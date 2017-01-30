# -*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

import sqlite3

url_home = 'http://www.dealmoon.com'
categories = ['Clothing-Jewelry-Bags',
              'Beauty',
              'Health-Personal-Care',
              'Nutrition-Supplements',
              'Baby',
              'Electronics']


def init_db(drop=False):
    with sqlite3.connect("dealmoon.db") as connection:
        c = connection.cursor()
        if drop:
            c.execute("DROP TABLE IF EXISTS deals")
        c.execute("CREATE TABLE IF NOT EXISTS deals (id INTEGER UNIQUE, category TEXT, title TEXT, url TEXT, image TEXT, favorites INTEGER)")


def store_data(url_home, categories):
    for category in ['Electronics']:  # categories:
        url_c = '/'.join([url_home, category])

        r = requests.get(url_c)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, "html5lib")

            # find all div tags with class attribute 'mlist'
            item_list = []
            for item in soup.find_all('div', {'class': 'mlist'}):

                mtxt = item.find('div', {'class': 'mtxt clearfix'})

                if mtxt.h1 or mtxt.h2:

                    h = mtxt.h1 or mtxt.h2
                    spans = h.a.find_all('span')
                    title = ' '.join([re.sub('\s+', ' ', span.text) for span in spans])
                    url = h.a['href']

                    src = item.find('div', {'class': 'img_wrap'}).a.img['src']

                    fav_num = item.find('em', {'class': 'fav-numbers'}).text or 0

                    # table deals: data-id, category, title, url, src, fav_num
                    item_list.append([item['data-id'], category, title, url, src, fav_num])

                else:
                    print mtxt

            with sqlite3.connect("dealmoon.db") as connection:
                c = connection.cursor()

                c.executemany('INSERT OR REPLACE INTO deals VALUES (?,?,?,?,?, ?)', item_list)


if __name__ == '__main__':
    init_db(drop=False)
    store_data(url_home, categories)
