from datetime import datetime
import json
from app import language
import requests
from app import app
from langdetect import detect
from flask import render_template, request
from flask_babel import gettext
import wikipedia
from search.get import Search_Data
import wikipedia

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(search_term):
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link        
    except:
        return None

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

        image = get_wiki_image(key)
            
        return title, link, summary, image
    except:
        return '', '', '', ''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    User = request.cookies.get('USERNAME')
    if User is None:
        User = gettext('Account')

    return render_template(
        '/index.html',
        User=User
    )

@app.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.args.get('q', '')
    type = request.args.get('tp', '')
    language_hl = request.args.get('hl', '')
    time_sr = request.args.get('tm', '')
    page = request.args.get('pg', '')
    
    wt = request.args.get('wt', '')
    wi = request.args.get('wi', '')
    ws = request.args.get('ws', '')
    wl = request.args.get('wl', '')

    if wt == '' or ws == '' or wl == '':
        wikipedia_info = get_wikipedia_info(keyword, language.get_locale())
    else:
        wikipedia_info = wt, wl, ws, wi
    
    if page == '' or page is None:
        page = 1
    else:
        page = int(page)

    if page == 1:
        prev_page_num = 1
    else:
        prev_page_num = page - 1

    next_page_num = page + 1

    search_result = Search_Data(type, keyword, page)

    if type == '':
        type = 'Text'
    if language_hl != '':
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

    if time_sr != '':
        time_sr = int(time_sr)
        filtered_data = []
        for item in search_result:
            item_time = datetime.strptime(item[7], '%a, %d %b %Y %H:%M:%S %Z')
            if item_time.year == time_sr:
                filtered_data.append(item)
        search_result = filtered_data

    language_list =  ['all', 'af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu', 'he', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi', 'zh-cn', 'zh-tw']
    time_list = ['all', '2022', '2023', '2024']

    User = request.cookies.get('USERNAME')
    if User is None:
        User = gettext('Account')

    if search_result == []:
        return render_template(
            '/search/index.html',
            User=User,
            query=keyword,
            languages = language_list,
            time=time_list,
            wikipedia_title = wikipedia_info[0],
            wikipedia_link = wikipedia_info[1],
            wikipedia_summary = wikipedia_info[2],
            wikipedia_image = wikipedia_info[3],
            note=gettext('No results found.'),
            prev_page = prev_page_num,
            next_page=next_page_num,
            results=search_result
        )
    else:
        return render_template(
            '/search/index.html',
            User=User,
            query=keyword,
            languages = language_list,
            time = time_list,
            wikipedia_title = wikipedia_info[0],
            wikipedia_link = wikipedia_info[1],
            wikipedia_summary = wikipedia_info[2],
            wikipedia_image = wikipedia_info[3],
            prev_page=prev_page_num,
            next_page=next_page_num,
            results=search_result,
        )