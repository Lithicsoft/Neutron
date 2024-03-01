from flask import Flask, request
from safe import escape_special_characters

import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join('./')))
from initializer.loader import database_loader

from ..dbmanager import select_from_information_longer,select_from_information_shorter

conn0 = database_loader(0)
conn1 = database_loader(1)
conn2 = database_loader(2)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def Search_Data():
    data = request.get_json()

    type = data['type']
    keyword = data['keyword']

    if type == 0:
        conn = conn0
    elif type == 1:
        conn = conn1
    elif type == 2:
        conn = conn2

    exact_match = re.findall(r'"(.*?)"', keyword)

    if exact_match:
        cursor = conn.cursor()

        safe_keyword = escape_special_characters(keyword)
        rows = select_from_information_longer(cursor, safe_keyword)
    else:
        cursor = conn.cursor()

        safe_keyword = escape_special_characters(keyword)
        rows = select_from_information_shorter(cursor, safe_keyword)
            
    if len(rows) == 0:
        return None
    else:
        return rows

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8500)
