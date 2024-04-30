from flask import Flask
from flask_babel import Babel
from app import language

app = Flask(__name__)
babel = Babel(app, locale_selector=language.get_locale)

from app import databases, ext, search, contribute, account
from manager import manager
from search import index