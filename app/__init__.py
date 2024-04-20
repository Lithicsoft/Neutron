from flask import Flask, request
from flask_babel import Babel

def get_locale():
    if request.args.get('lang'):
        return request.args.get('lang')

    return request.accept_languages.best_match(LANGUAGES.keys())

app = Flask(__name__)
babel = Babel(app, locale_selector=get_locale)

LANGUAGES = {
    'en': 'English',
    'vi': 'Vietnamese'
}

from app import ext, search, contribute, account
