from app import app
from flask import render_template

@app.route('/result.js')
def result_js():
    return render_template(
        '/result.js'
    )

@app.route('/search/script.js')
def search_js():
    return render_template(
        '/search/script.js'
    )

@app.route('/search.js')
def search_suggestions_js():
    return render_template(
        '/search.js'
    )

@app.route('/search.css')
def searcH_css():
    return render_template(
        '/search.css'
    )

@app.route('/log.txt')
def log_txt():
    return render_template(
        '/log.txt'
    )