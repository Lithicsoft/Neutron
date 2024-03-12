from app import app
from langdetect import detect
from flask import render_template, request
import wikipedia
from search.get import Search_Data

import wikipedia

def get_wikipedia_title(key, language):
    try:
        if language == '':
            wikipedia.set_lang('en')
        else:
            wikipedia.set_lang(language)
        
        page = wikipedia.page(key)
        return page.title
    except:
        return ''

def get_wikipedia_link(key, language):
    try:
        if language == '':
            wikipedia.set_lang('en')
        else:
            wikipedia.set_lang(language)
    
        page = wikipedia.page(key)
        return page.url
    except:
        return ''

def get_wikipedia_summary(key, language):
    try:
        if language == '':
            wikipedia.set_lang('en')
        else:
            wikipedia.set_lang(language)

        summary = wikipedia.summary(key, sentences=2)
        return summary
    except:
        return ''

def get_wikipedia_image(key):
    try:
        page = wikipedia.page(key)
        image_url = page.images[0]
        return image_url
    except:
        return ''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template(
        '/index.html',
    )

@app.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.args.get('q', '')
    type = request.args.get('tp', '')
    language_hl = request.args.get('hl', '')

    search_result = []

    if type == '':
        type = 'Text'
    if language_hl != '':
        search_result = Search_Data(type, keyword)
        filtered_data = []
        for item in search_result:
            try:
                language1 = detect(item[1])
                language2 = detect(item[5])
            except:
                continue 
            
            if language1 == language_hl or language2 == language_hl:
                filtered_data.append(item)
            search_result = filtered_data
    else:
        search_result = Search_Data(type, keyword) 

    if search_result == []:
        return render_template(
            '/search/index.html',
            query=keyword,
            languages = ['all', 'af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu', 'he', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi', 'zh-cn', 'zh-tw'],
            wikipedia_title = get_wikipedia_title(keyword, language_hl),
            wikipedia_link = get_wikipedia_link(keyword, language_hl),
            wikipedia_summary = get_wikipedia_summary(keyword, language_hl),
            wikipedia_image = get_wikipedia_image(keyword),
            note='No results found.'
        )
    else:
        return render_template(
            '/search/index.html',
            query=keyword,
            languages = ['all', 'af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu', 'he', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi', 'zh-cn', 'zh-tw'],
            wikipedia_title = get_wikipedia_title(keyword, language_hl),
            wikipedia_link = get_wikipedia_link(keyword, language_hl),
            wikipedia_summary = get_wikipedia_summary(keyword, language_hl),
            wikipedia_image = get_wikipedia_image(keyword),
            results=search_result
        )