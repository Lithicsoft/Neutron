from datetime import datetime
import argparse
from app import app
from waitress import serve
from log.write import sys_log

def main(dev_mode=False):
    if dev_mode:
        print("Running in dev mode...")
        app.run(host='0.0.0.0', port=50100, debug=True)
    serve(app, host='0.0.0.0', port=50100, url_scheme='https')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", help="Switch to dev mode", action="store_true")
    args = parser.parse_args()

    sys_log('Start Server', str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("The server is active...")

    main(args.dev)
