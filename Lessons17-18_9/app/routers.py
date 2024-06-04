from app import app, db # from __init__ import app
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, Poll, Option

@app.route('/')
def home():
    polls = db.session.scalars(sa.select(Poll)).all()
    return render_template('home.html', polls=polls) 


@app.route('/poll/<int:id>')
def options_list(id):
    options = db.session.scalars(sa.select(Option).where(Option.poll_id == id)).all()
    poll = db.session.scalar(sa.select(Poll).where(Poll.id == id))
    return render_template('options_list.html', options=options, poll=poll)

