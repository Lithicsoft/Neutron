from app import app
from flask import render_template, request

from search.get import Search_Data

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template(
        'index.html',
    )

@app.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.args.get('q', '')
    type = request.args.get('type', '')
    if type == '':
        type = 'Text'
    return render_template(
        'search/index.html',
        results=Search_Data(type, keyword)
    )