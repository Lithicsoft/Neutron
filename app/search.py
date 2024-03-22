from datetime import datetime
from bs4 import BeautifulSoup
import requests
from app import app
from langdetect import detect
from flask import render_template, request
import wikipedia
from search.get import Search_Data
import wikipedia

def get_wikipedia_info(key, language=''):
    try:
        if language == '':
            wikipedia.set_lang('en')
        else:
            wikipedia.set_lang(language)

        page = wikipedia.page(key)
        title = page.title
        link = page.url
        summary = wikipedia.summary(key, sentences=2)

        image = ''
        if page.images:
            image = page.images[0]
            
        return title, link, summary, image
    except:
        return '', '', '', ''

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
    time = request.args.get('tm', '')
    page = request.args.get('pg', '')

    if page == '' or page is None:
        page = 1
    else:
        page = int(page)

    if page == 1:
        prev_page_num = 1
    else:
        prev_page_num = page - 1

    next_page_num = page + 1

    search_result = []

    if type == '':
        type = 'Text'
    if language_hl != '':
        search_result = Search_Data(type, keyword, page)
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
        search_result = Search_Data(type, keyword, page) 

    if time != '':
        time = int(time)
        filtered_data = []
        for item in search_result:
            item_time = datetime.strptime(item[7], '%a, %d %b %Y %H:%M:%S %Z')
            if item_time.year == time:
                filtered_data.append(item)
        search_result = filtered_data

    language_list =  ['all', 'af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu', 'he', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi', 'zh-cn', 'zh-tw']
    time_list = ['all', '2022', '2023', '2024']

    wikipedia_info = get_wikipedia_info(keyword, language_hl)

    if search_result == []:
        return render_template(
            '/search/index.html',
            query=keyword,
            languages = language_list,
            time = time_list,
            wikipedia_title = wikipedia_info[0],
            wikipedia_link = wikipedia_info[1],
            wikipedia_summary = wikipedia_info[2],
            wikipedia_image = wikipedia_info[3],
            note='No results found.',
            prev_page = prev_page_num,
            next_page=next_page_num,
            results=search_result
        )
    else:
        return render_template(
            '/search/index.html',
            query=keyword,
            languages = language_list,
            time = time_list,
            wikipedia_title = wikipedia_info[0],
            wikipedia_link = wikipedia_info[1],
            wikipedia_summary = wikipedia_info[2],
            wikipedia_image = wikipedia_info[3],
            prev_page=prev_page_num,
            next_page=next_page_num,
            results=search_result
        )