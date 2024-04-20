from flask import request

LANGUAGES = {
    'en': 'English',
    'vi': 'Vietnamese'
}

def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

def prompt():
    if get_locale() == 'en':
        prompt = ' (Please summarize the answer)'
    elif get_locale() == 'vi':
        prompt = ' (Hãy tóm tắt câu trả lời)'
    
    return prompt