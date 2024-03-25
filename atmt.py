import getpass
import hashlib
import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin

from manager.call import manager_insert_data, manager_get_id, manager_remove_data, manager_edit_data

def summarize_text(text, max_length=174):
    if len(text) <= max_length:
        return text
    else:
        last_space_index = text.rfind(' ', 0, max_length)
        return text[:last_space_index] + '...'

def get_website_info(url, headers):
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.title.string.strip() if soup.title else ''

            tags_to_extract = ['p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'strong', 'em', 'blockquote', 'cite', 'q', 'dfn', 'abbr', 'time', 'code', 'var', 'samp', 'kbd', 'sub', 'sup', 'i', 'b', 'u', 'mark', 'small', 'del', 'ins', 's']
            text_content = ' '.join([tag.get_text().strip() for tag in soup.find_all(tags_to_extract)])

            description = soup.select_one('meta[name="description"]')['content'] if soup.select_one('meta[name="description"]') else ''

            keywords = soup.select_one('meta[name="keywords"]')['content'] if soup.select_one('meta[name="keywords"]') else ''

            return {
                "title": title,
                "text_content": text_content,
                "description": description,
                "keywords": keywords
            }
        else:
            return None
    except Exception as e:
        print(f"Error when getting website info from {url}: {e}")
        return None

username = input('Username: ')
password = getpass.getpass('Password: ')
password = hashlib.md5(hashlib.sha256(password.encode('utf-8')).hexdigest().encode()).hexdigest()
link_to_crawl = input('Url: ')

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537.36'
headers = {'User-Agent': user_agent}
investigation_list = deque([link_to_crawl])

while investigation_list:
    url = investigation_list.popleft()
    print("Investigating url: ", url)
    website_info = get_website_info(url, headers)
    if website_info is not None:
        print("Title: ", website_info["title"])
        type = "Text"
        result = manager_insert_data(type, username, password, url, website_info["title"], website_info["text_content"], website_info["description"], website_info["keywords"], summarize_text(website_info["text_content"]))
        if result == "Content already exists in the database.":
            site_id = manager_get_id(type, url)
            print(manager_edit_data(type, username, password, site_id, url, website_info["title"], website_info["text_content"], website_info["description"], website_info["keywords"], summarize_text(website_info["text_content"])))
        else:
            print(result)
        print("---------")

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = soup.select('a[href]')
            for link in search_results:
                new_url = urljoin(url, link.get('href'))
                if new_url not in investigation_list:
                    investigation_list.append(new_url)
    else:
        type = "Text"
        site_id = manager_get_id(type, url)
        if site_id is not None:
            print(manager_remove_data(type, username, password, site_id))
