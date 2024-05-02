from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubs.db'

db = SQLAlchemy(app)

class Clubs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    coach = db.Column(db.String(40), nullable=True)
    wins_ucl = db.Column(db.Integer, nullable=True)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=True)
    content = db.Column(db.String(200), nullable=True)
    team = db.Column(db.String(30), db.ForeignKey('clubs.id'))
    date = db.Column(db.String())



@app.route('/')
def home():
    clubs=Clubs.query.all()
    return render_template('index.html', clubs=clubs)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/club/<int:id>')
def club_detail(id):
    if id > len(clubs):
        return redirect(url_for('home'))
    return render_template('club_detail.html', club=clubs[id-1])



@app.route('/biggest_winner')
def the_biggest_winner():
    return render_template('winner_ucl.html', clubs=clubs)

# club add 

@app.route('/club/add')
def add_club():
    return render_template('add_club.html')

@app.route('/add_club_handler', methods=['POST', 'GET'])
def add_club_hand():
    # name = request.form.get("name", 'error')
    # coach = request.form.get("coach", 'error')
    # wins_ucl = request.form.get("wins_ucl", 'error')
    

    if request.method == 'POST':
        club = Clubs(name=request.form.get('name'), coach=request.form.get('coach'), wins_ucl=request.form.get('wins_ucl'))
        print(club)
        db.session.add(club)
        db.session.commit()
        return redirect(url_for('home'))
    return redirect(url_for('add_club'), error='error')


# register

@app.route('/register')
def register():
    return render_template('register.html', error=False)


@app.route('/register_handler', methods=['POST', 'GET'])
def reg_handler():
    db = SQLite('clubs.db')
    username = request.form.get("username", 'error')
    password = request.form.get("password", 'error')
    email = request.form.get("email", 'error')
    if '@' in email or db.valid_username(username):
        if request.method == 'POST':
            db.write_user(username, password, email)
            return redirect(url_for('home'))
    else:
        error = "Неправильно введено пошту або таке ім'я вже існує" 
        return render_template('register.html', error=error)

@app.errorhandler(404)
def error404(error):
    return render_template('error404.html'), 404


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)