from app import app
from waitress import serve

def main():
    serve(app, host='0.0.0.0', port=50100, url_scheme='https')

if __name__ == '__main__':
    print("The server is active...")
    main()
    