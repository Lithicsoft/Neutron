from flask import Flask, jsonify, request

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
    page = int(data['page'])

    exact_match = re.findall(r'"(.*?)"', keyword)

    if exact_match:
        cursor = conn.cursor()

        rows = Library_Exact_Search(cursor, type, keyword, page)
    else:
        cursor = conn.cursor()

        rows = Library_Full_Text_Search(cursor, type, keyword, page)
    
    if len(rows) == 0:
        return jsonify([])
    else:
        return rows

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8500)
