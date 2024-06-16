#!/usr/bin/env python3
"""
0. Basic Flask app
"""

from flask import Flask, render_template, request
from flask_babel import Babel


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
    local = request.args.get('locale', 'en')
    return request.accept_languages.best_match(local)


@app.route('/')
def index() -> str:
    """ Route app """
    local = get_locale()
    return render_template('3-index.html', local=local)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
