from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

clubs = [
    {'id': 1, 'name': 'FC Barcelona', 'coach': 'Xavi Hernández', 'wins_ucl': 5},
    {'id': 2, 'name': 'Real Madrid', 'coach': 'Carlo Ancelotti', 'wins_ucl': 14},
    {'id': 3, 'name': 'Manchester City', 'coach': 'Pep Guardiola ', 'wins_ucl': 1},
    {'id': 4, 'name': 'Arsenal', 'coach': 'Mikel Arteta', 'wins_ucl': 3},
]


@app.route('/')
def home():
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


@app.errorhandler(404)
def error404(error):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)