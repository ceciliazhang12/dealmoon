# -*- coding:utf-8 -*-

from __future__ import print_function

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

import sqlite3
from datetime import datetime
import time
from threading import Thread
import schedule
from db import init_db, get_data

url_home = 'http://www.dealmoon.com'
categories = ['Clothing-Jewelry-Bags',
              'Beauty',
              'Health-Personal-Care',
              'Baby',
              'Electronics']

app = Flask(__name__)
Bootstrap(app)


def run_every_10_minutes():
    print("task run at {}".format(datetime.now()))
    get_data(url_home, categories)


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


@app.route("/")
def home():

    with sqlite3.connect("dealmoon.db") as connection:
        c = connection.cursor()
        top_items = {}
        for category in categories:
            c.execute("SELECT * FROM deals WHERE category = '{}' ORDER BY favorites DESC LIMIT 8".format(category))
            items = c.fetchall()
            category_shortened = category.split('-')[0]
            top_items[category_shortened] = items

        now = str(datetime.now())

    return render_template("index.html", now=now, categories=categories, **top_items)


if __name__ == "__main__":
    # schedule.every(10).minutes.do(run_every_10_minutes)
    # t = Thread(target=run_schedule)
    # t.start()
    app.run(debug=True)
