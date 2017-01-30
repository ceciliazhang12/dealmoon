# -*- coding:utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import sqlite3

categories = ['Clothing-Jewelry-Bags', \
              'Beauty', \
              'Health-Personal-Care', \
              'Nutrition-Supplements', \
              'Baby', \
              'Home-Garden', \
              'Electronics'] 

app = Flask(__name__)

@app.route("/")
def home():
    with sqlite3.connect("dealmoon.db") as connection:
        c = connection.cursor()
        for category in ['Electronics']:  # categories:
            c.execute("SELECT * FROM deals WHERE category = '{}' ORDER BY favorites LIMIT 10".format(category))
            top_items = c.fetchall()

    return render_template("index.html", item='I love Cecilia') # render a template

if __name__ == "__main__":
    app.run(debug=True)