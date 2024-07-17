from app import app, db, login # from __init__ import app
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, Poll, Option, Category

@app.route('/')
def home():
    polls = db.session.scalars(sa.select(Poll)).all()
    categories = db.session.scalars(sa.select(Category)).all()
    return render_template('home.html', polls=polls, categories=categories) 


@app.route('/profile')
@login_required
def profile():
    user_polls = db.session.scalars(current_user.voted_polls.select()).all()
    return render_template('profile.html', polls=user_polls)


@app.route('/poll/<int:poll_id>')
def options_list(poll_id):
    options = db.session.scalars(sa.select(Option).where(Option.poll_id == poll_id)).all()
    poll = db.session.scalar(sa.select(Poll).where(Poll.id == poll_id))
    return render_template('options_list.html', options=options, poll=poll)


@app.route('/<int:poll_id>/options/<int:option_id>')
@login_required
def add_vote(poll_id, option_id):
    poll = db.session.get(Poll, poll_id)
    user_polls = db.session.scalars(current_user.voted_polls.select()).all()
    option = db.session.scalar(sa.select(Option).where(Option.id == option_id)) 
    if poll in user_polls:
        error = 'You are already voted'
        return redirect(url_for('options_list', poll_id=poll_id, error=error))
    option.votes += 1
    current_user.voted_polls.add(poll)
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


# register/login/logout

@login.user_loader
def user_loader(id):
    return db.session.get(User, id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return '<h2> Log out please </h2>'
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User(username=username, email=email)
        user.set_password(password)
        users = db.session.scalars(sa.select(User)).all()
        if user in users:
            return redirect(url_for('register'))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return '<h2> Log out please </h2>'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if not user or not user.check_password(password):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))