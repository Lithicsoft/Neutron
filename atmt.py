import requests
from bs4 import BeautifulSoup
from initializer.loader import database_loader
from manager.insert import insert_data

def summarize_text(text, max_length=100):
    if len(text) <= max_length:
        return text
    else:
        last_space_index = text.rfind(' ', 0, max_length)
        return text[:last_space_index] + '...'

def get_website_info(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.title.string.strip()

            text_content = ''
            for paragraph in soup.find_all(['p', 'div']):
                text_content += paragraph.get_text().strip() + '\n'

            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description['content'] if meta_description else ''

            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            keywords = meta_keywords['content'] if meta_keywords else ''

            return {
                "title": title,
                "text_content": text_content,
                "description": description,
                "keywords": keywords
            }
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

def ATMT_STRT(random_keyword):
    conn = database_loader()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537.36'
    headers = {'User-Agent': user_agent}
    search_url = f"https://www.google.com/search?q={random_keyword}&hl=en"

    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('a')
        random_urls = [link.get('href') for link in search_results if link.get('href') and link.get('href').startswith('http')]

        for url in random_urls:
            print("url: ", url)
            website_info = get_website_info(url)
            if website_info is None:
                pass
            else:
                print("title: ", website_info["title"])
                insert_data(conn, url, website_info["title"], website_info["text_content"], website_info["description"], website_info["keywords"], summarize_text(website_info["text_content"]))
                print("---PASS---")
    else:
        print("ERR.")
