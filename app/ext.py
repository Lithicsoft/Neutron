from app import app
from flask import render_template

@app.route('/result.js')
def result_js():
    return render_template(
        '/result.js'
    )

@app.route('/search/script.js')
def searcH_js():
    return render_template(
        '/search/script.js'
    )

@app.route('/search.css')
def searcH_css():
    return render_template(
        '/search.css'
    )

@app.route('/contribute/tab.css')
def tab_css():
    return render_template(
        '/contribute/tab.css'
    )

@app.route('/contribute/tab.js')
def tab_js():
    return render_template(
        '/contribute/tab.js'
    )