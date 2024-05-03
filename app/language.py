from flask import request

LANGUAGES = {
    'en': 'English',
    'vi': 'Vietnamese',
    'hr': 'Croatian'
}

def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())
