import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required


app = Flask(__name__, )
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
app.config['SECRET_KEY'] = '123456789'

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=True, unique=True)
    password = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(30), nullable=True, unique=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username", 'error')
        password = request.form.get("password", 'error')
        email = request.form.get("email", 'error')
        print(username, password, email)
        new_user = User(username=username, password=generate_password_hash(password), email=email)
        db.session.add(new_user)
        db.session.commit()
        return render_template('home.html')    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        email = request.form.get("email", 'error')
        password = request.form.get("password", 'error')
        user = User.query.filter_by(email=email).first()
        if not user or  not check_password_hash(user.password, password):
            return render_template('login.html', error='Error')    
        login_user(user)
        return render_template('home.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('logout_ok'))

@app.route('/logout_ok')
def logout_ok():
    return '<h1>Logout ok</h1>'


@app.route('/weather')
@login_required
def weather():
    result = requests.get('https://api.openweathermap.org/data/2.5/weather', 
                          params={'q':'Lviv', 'appid': 'df2705df9ca9fd4f806c153f9a4b9b9c', 'lang': 'ua', 'units': 'metric'  })
    weather = result.json()
    temp = weather['main']['temp']
    wind_speed = weather['wind']['speed']
    print(temp)
    return  render_template('weather.html', temp=temp, wind_speed=wind_speed)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
