from flask import request

LANGUAGES = {
    'en': 'English',
    'vi': 'Vietnamese'
}

def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())
