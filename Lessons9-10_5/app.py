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

@app.route('/post/<int:id>')
def post_by_id(id):
    post = Posts.query.get_or_404(id)
    return render_template('/post_detail.html', post=post)


@app.route('/posts/category/<int:category_id>')
def posts_by_category(category_id):
    posts = Posts.query.filter_by(category=category_id)
    category = Category.query.get_or_404(category_id)
    return render_template('post_by_category.html', posts=posts, category=category)


@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)