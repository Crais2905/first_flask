from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/students')
def posts():
    return render_template('students.html')


@app.route('/Lisovets')
def lisovets():
    return render_template('lisovets.html')


@app.route('/Stroman')
def stroman():
    return render_template('stroman.html')


@app.route('/Vasylchuk')
def vasylchuk():
    return render_template('vasylchuk.html')


if __name__ == '__main__':
    app.run(debug=True)