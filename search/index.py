from flask import Flask, jsonify, request
from safe import escape_special_characters

import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join('./')))
from library.database import Library_Exact_Search, Library_Full_Text_Search
from initializer.loader import database_loader

conn = database_loader()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def Search_Data():
    data = request.get_json()

    type = data['type']
    keyword = data['keyword']

    exact_match = re.findall(r'"(.*?)"', keyword)

    if exact_match:
        cursor = conn.cursor()

        safe_keyword = escape_special_characters(keyword)

        rows = Library_Exact_Search(cursor, type, safe_keyword)
    else:
        cursor = conn.cursor()

        safe_keyword = escape_special_characters(keyword)

        rows = Library_Full_Text_Search(cursor, type, safe_keyword)
            
    if len(rows) == 0:
        return jsonify([])
    else:
        return rows

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8500)
