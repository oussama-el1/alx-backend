#!/usr/bin/env python3
"""
0. Basic Flask app
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """ get a user based on id """
    return users.get(int(user_id), 0)


class Config:
    """ class that has a LANGUAGES class attribute """
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"
    LANGUAGES = ["en", "fr"]


app = Flask(__name__)
app.config.from_object(Config)
app.config['BABEL_DEFAULT_LOCALE'] = Config.BABEL_DEFAULT_LOCALE
app.config['BABEL_DEFAULT_TIMEZONE'] = Config.BABEL_DEFAULT_TIMEZONE
babel = Babel(app)


@babel.localeselector
def get_locale():
    """ select the langueage based on the header http """
    locale = request.args.get('locale', '').strip()
    if locale and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(Config.LANGUAGES)


@app.before_request
def before_request():
    """ before request to get the login user before request"""
    loged_in = request.args.get('login_as', 0)
    setattr(g, 'user', get_user(loged_in))


@app.route('/')
def index() -> str:
    """ Route app for the Flask app"""
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
