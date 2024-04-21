from flask import request

LANGUAGES = {
    'en': 'English',
    'vi': 'Vietnamese'
}
prompt_list = [' (Please summarize your answer)', ' (Vui lòng tóm tắt câu trả lời của bạn)']

def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

def prompt():
    if get_locale() == 'en':
        prompt = prompt_list[0]
    elif get_locale() == 'vi':
        prompt = prompt_list[1]
    
    return prompt