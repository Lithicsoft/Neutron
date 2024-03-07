from app import app
from flask import render_template

@app.route('/search/script.js')
def searcH_js():
    return render_template(
        '/contribute/script.js'
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