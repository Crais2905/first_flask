from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, )
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    decription = db.Column(db.String(100))


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=True)
    decription = db.Column(db.String(200))
    author = db.Column(db.String(20), nullable=True)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/posts')
def posts():
    posts = Posts.query.all()
    return render_template('posts.html', posts=posts)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)