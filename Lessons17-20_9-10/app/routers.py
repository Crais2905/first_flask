from app import app, db # from __init__ import app
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, Poll, Option, Category

@app.route('/')
def home():
    polls = db.session.scalars(sa.select(Poll)).all()
    categories = db.session.scalars(sa.select(Category)).all()
    return render_template('home.html', polls=polls, categories=categories) 


@app.route('/poll/<int:poll_id>')
def options_list(poll_id):
    options = db.session.scalars(sa.select(Option).where(Option.poll_id == poll_id)).all()
    poll = db.session.scalar(sa.select(Poll).where(Poll.id == poll_id))
    return render_template('options_list.html', options=options, poll=poll)


@app.route('/<int:poll_id>/options/<int:option_id>')
def add_vote(poll_id, option_id):
    option = db.session.scalar(sa.select(Option).where(Option.id == option_id)) 
    option.votes += 1
    db.session.add(option)
    db.session.commit()
    return redirect(url_for('options_list', poll_id=poll_id))


@app.route('/category/<int:category_id>')
def category_polls(category_id):
    category = db.session.get(Category, category_id)
    print(category)
    polls = db.session.scalars(sa.select(Poll).where(Poll.category_id == category_id))
    return render_template('category_polls.html', category=category, polls=polls)


# add poll

@app.route('/add-poll', methods=['GET', 'POST'])
def add_poll():
    categories = db.session.scalars(sa.select(Category)).all()
    if request.method == 'POST':
        topic = request.form.get('topic')
        category_id = int(request.form.get('category'))
        category = db.session.get(Category, category_id)

        
        poll = Poll(topic=topic, category=category)
        db.session.add(poll)
        db.session.commit()
        return redirect(url_for('add_option', poll_id=poll.id))
    return render_template('add_poll.html', categories=categories)


@app.route('/add-poll/<int:poll_id>/options', methods=['GET', 'POST'])
def add_option(poll_id):
    options = db.session.scalars(sa.select(Option).where(Option.poll_id == poll_id))
    if request.method == 'POST':
        title = request.form.get('title')

        option = Option(title=title, poll_id=poll_id)
        db.session.add(option)
        db.session.commit()
        return redirect(url_for('add_option', poll_id=poll_id, options=options))
    return render_template('add_option.html', options=options, poll_id=poll_id)