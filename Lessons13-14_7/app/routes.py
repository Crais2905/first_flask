from app import app # from __init__ import app
from flask import render_template, url_for



@app.route('/')
def home():
    return render_template('home.html') 