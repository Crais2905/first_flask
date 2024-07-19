from app import app, db, login  # from __init__ import app
from flask import render_template, url_for, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
import sqlalchemy as sa
import sqlalchemy.orm as os
from app.models import User, Tour
from datetime import datetime
from .forms import TourForm, RegistrationForm, LoginForm


@app.route('/')
def home():
    tours = db.session.scalars(sa.select(Tour)).all()
    time = datetime.now()
    return render_template('home.html', tours=tours, now_time=time) 


@app.route('/tour/new', methods=['GET', 'POST'])
def new_tour():
    form = TourForm()
    if form.validate_on_submit():
        tour = Tour(
            title=form.title.data,
            decription=form.decription.data,
            price=form.price.data,
            country=form.country.data,
            time=form.time.data
        )
        db.session.add(tour)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_tour.html', form=form) 


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
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('home'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return '<h2> Log out please </h2>'
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if not user or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/root')
def root():
    pass