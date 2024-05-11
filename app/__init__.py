import os
from flask import Flask
from flask_babel import Babel
from app import language

frontend_dir = os.path.join("./", 'frontend')
app = Flask(__name__, template_folder=frontend_dir)
babel = Babel(app, locale_selector=language.get_locale)

from app import databases, ext, search, contribute, account
from manager import manager
from search import index