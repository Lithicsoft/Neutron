from flask import jsonify, request
from app import app, databases
import re
import wikipedia
from library.database import Library_Full_Text_Domain_Search, Library_Full_Text_Search

@app.route('/api/search', methods=['POST'])
def Search_Data():
    conn = databases.conn
    
    data = request.get_json()

    type = data['type']
    keyword = data['keyword']
    page = int(data['page'])

    domain_match = re.search(r'site:(\\S+)', keyword)

    cursor = conn.cursor()

    if domain_match:
        domain = domain_match.group(1)
        rows = Library_Full_Text_Domain_Search(cursor, type, keyword, domain, page)
    else:
        rows = Library_Full_Text_Search(cursor, type, keyword, page)
    
    if len(rows) == 0:
        return jsonify([])
    else:
        return rows
    
@app.route('/api/search/suggestions', methods=['POST'])
def Search_Suggestions():
    data = request.get_json()
    return wikipedia.search(data['keyword']) if data['keyword'] else []
