from flask import Flask, jsonify, request
from waitress import serve
import re
from library.database import Library_Full_Text_Domain_Search, Library_Full_Text_Search
from initializer.loader import database_loader

app = Flask(__name__)

@app.route('/', methods=['POST'])
def Search_Data():
    conn = database_loader()
    
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

def main():
    serve(app, host='0.0.0.0', port=8500)

if __name__ == '__main__':
    main()
