from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = [
    {'username': 'WorldClass_soccer_player', 'name': '손흥민'},
    {'username': 'Legendary_basketball_player', 'name': 'Michael Jordan'},
    {'username': 'Tennis_champion', 'name': 'Serena Williams'}
]

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)