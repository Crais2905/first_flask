from app import app, db, login  # from __init__ import app
from flask import render_template, url_for, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
import sqlalchemy as sa
import sqlalchemy.orm as os
from app.models import User, Tour
from datetime import datetime


@app.route('/')
def home():
    tours = db.session.scalars(sa.select(Tour)).all()
    time = datetime.now()
    return render_template('home.html', tours=tours, now_time=time) 


@login.user_loader
def user_loader(id):
    return db.session.get(User, id)


@app.route('/tour/<int:tour_id>')
def full_tour(tour_id):
    tour = db.session.get(Tour, tour_id)
    return render_template('full_tour.html', tour=tour)


@app.route('/tour/<int:tour_id>/book')
def book_tour(tour_id):
    tour = db.session.scalars(sa.select(Tour).where(Tour.id == tour_id)).first()
    user_tours = db.session.scalars(current_user.bought_tours.select()).all()
    if tour in user_tours:
        return redirect(url_for('full_tour', tour_id=tour.id, error='You already book this tour'))
    current_user.bought_tours.add(tour)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    tours = db.session.scalars(current_user.bought_tours.select()).all()
    return render_template('profile.html', tours=tours)



# register/login/logout

@login.user_loader
def user_loader(id):
    return db.session.get(User, id)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return '<h2> Log out please </h2>'
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        user = db.session.scalar(sa.select(User).where(User.username == new_user.username))
        if user:
            return redirect(url_for('registration'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('registration.html')


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