# -*- coding:utf-8 -*-

from flask import Flask, render_template, url_for
from functools import wraps
import sqlite3

categories = ['Clothing-Jewelry-Bags',
              'Beauty',
              'Health-Personal-Care',
              'Nutrition-Supplements',
              'Baby',
              'Electronics']

app = Flask(__name__)

@app.route("/")
def home():
    with sqlite3.connect("dealmoon.db") as connection:
        c = connection.cursor()
        for category in ['Electronics']:  # categories:
            c.execute("SELECT * FROM deals WHERE category = '{}' ORDER BY favorites LIMIT 10".format(category))
            top_items = c.fetchall()

    return render_template("index.html", categories=categories, top_items=top_items)


if __name__ == "__main__":
    app.run(debug=True)
