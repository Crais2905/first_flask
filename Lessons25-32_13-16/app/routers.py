from app import app, db, login  # from __init__ import app
from flask import abort, render_template, url_for, request, redirect, jsonify
from flask_login import login_user, logout_user, current_user
import sqlalchemy as sa
import sqlalchemy.orm as os
from .forms import LoginForm, RegistrationForm, AddCategoryForm, PostForm
# from flask_restful import Api, Resource, reqparse
from app.models import User, Category, Post
import logging


@app.route('/')
def home():
    posts = db.session.scalars(sa.select(Post))
    return render_template('home.html', posts=posts)

#category/post

@app.route('/categories')
def categories():
    categories = db.session.scalars(sa.select(Category))
    return render_template('categories.html', categories=categories)


@app.route('/category/<int:category_id>/posts')
def category_posts(category_id):
    posts = db.session.scalars(sa.select(Post).where(Post.category_id == category_id))
    return render_template('home.html', posts=posts)




@app.route('/category/new', methods=['GET', 'POST'])
def new_category():
    form = AddCategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new_category.html', form=form)



@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    form.category.choices = [(category.id, category.name) for category in (db.session.scalars(sa.select(Category)))]
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, category_id=form.category.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new_post.html', form=form)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    form = PostForm()
    form.category.choices = [(category.id, category.name) for category in (db.session.scalars(sa.select(Category)))]
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category_id = form.category.data

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data =  post.title
        form.content.data = post.content
        form.category.data = post.category_id
        
    return render_template('new_post.html', form=form)


# login/registration
@app.route('/profile')
def profile():
    posts = db.session.scalars(current_user.user_posts.select())
    return render_template('profile.html', posts=posts)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
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
def logout():
    logout_user()
    return redirect(url_for('home'))