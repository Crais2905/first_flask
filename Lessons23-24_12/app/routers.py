from app import app, db, login  # from __init__ import app
from flask import render_template, url_for, request, redirect, jsonify
from flask_login import login_user, logout_user, current_user
import sqlalchemy as sa
import sqlalchemy.orm as os
from flask_restful import Api, Resource, reqparse
from app.models import Post, Category
import json 

def initialize_routes(api: Api):
    api.add_resource(PostListResource, '/posts')
    api.add_resource(PostResource, '/posts/<int:id>')
    api.add_resource(CategoryResource, '/category/<int:id>')
    api.add_resource(CategoryListResource, '/categories')


class CategoryListResource(Resource):
    def get(self):
        categories = db.session.scalars(sa.select(Category)).all()
        return [{'id': cat.id, 'name': cat.name} for cat in categories]

    def post(self):
        parcer = reqparse.RequestParser()
        parcer.add_argument('name', required=True, help='Name can not be blank')
        args = parcer.parse_args()
        
        category = Category(name=args['name'])
        db.session.add(category)
        db.session.commit()
        return [{'Category': {
                      'id': category.id,
                      'name': category.name
                  }}], 201


class CategoryResource(Resource):
    def get(self, id):
        category = db.session.query(Category).get_or_404(id)
        return {'id': category.id, 'name': category.name}

    def put(self, id):
        parcer = reqparse.RequestParser()
        parcer.add_argument('name', required=True, help='Name can not be blank')
        args = parcer.parse_args()
        category = db.session.query(Category).get_or_404(id)

        category.name = args['name']


        db.session.commit()
        return [{'Category': {
                'id': category.id,
                'name': category.name
            }}], 201


    def delete(self):
        pass

class PostListResource(Resource):
    def get(self):
        posts = db.session.query(Post).all()
        return [{'id': post.id, 'name': post.name, 'content': post.content, 'category': str(post.category)} for post in posts]
        

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name can not be blank')
        parser.add_argument('content', required=True, help='Content can not be blank')
        parser.add_argument('category_id', required=True, help='Catgory id can not be blank')
        args = parser.parse_args()

        post = Post(name=args['name'], content=args['content'], category_id=args['category_id'])
        db.session.add(post)
        db.session.commit()
        return {'Post': {
                'id': post.id,
                'name': post.name,
                'content': post.content,
                'category': str(post.category)
            }}, 201
    

class PostResource(Resource):
    def get(self, id):
        post = db.session.query(Post).get_or_404(id)
        return  {'Post': {
                'id': post.id,
                'name': post.name,
                'content': post.content,
                'category': str(post.category)
            }}
    

    def put(self, id):
        parser = reqparse.RequestParser()
        post = db.session.query(Post).get_or_404(id)
        parser.add_argument('name', required=True, help='Name can not be blank')
        parser.add_argument('content', required=True, help='Content can not be blank')
        parser.add_argument('category_id', required=True, help='Catgory id can not be blank')
        args = parser.parse_args()

        post.name = args['name']
        post.content = args['content']
        post.category_id = args['category_id']

        db.session.commit()

        return  {'Post': {
            'id': post.id,
            'name': post.name,
            'content': post.content,
            'category': str(post.category)
        }}
    