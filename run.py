from datetime import datetime
from app import app
from waitress import serve

from log.write import sys_log

def main():
    serve(app, host='0.0.0.0', port=50100, url_scheme='https')

if __name__ == '__main__':
    sys_log('Start Server', str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("The server is active...")
    main()
    