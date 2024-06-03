from app import app, db,  login  # from __init__ import app
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user
import sqlalchemy as sa
import sqlalchemy.orm as os
from app.models import User, Post


@app.route('/')
def home():
    return render_template('home.html') 


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    if current_user.is_authenticated:
        return render_template('home.html')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password') 
        user = db.session.scalar(sa.select(User).where(User.email == email))

        if not user or not user.check_password(password):
            return render_template('log_in.html')
        
        login_user(user)
        return redirect(url_for('home'))
    return render_template('log_in.html')


@app.route('/log_out')
def log_out():
    logout_user()
    return redirect(url_for('home'))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password') 
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('sign_up.html')