import hashlib
import os
import re
from urllib import response
import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin, urlparse

from manager.call import manager_insert_data, manager_get_id, manager_remove_data, manager_edit_data

def summarize_text(text, max_length=174):
    if len(text) <= max_length:
        return text
    else:
        last_space_index = text.rfind(' ', 0, max_length)
        return text[:last_space_index] + '...'

def classify_website(url):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']
    if any(url.endswith(ext) for ext in image_extensions):
        return 'Image'
    elif 'youtube.com/watch' in url:
        return 'Video'
    else:
        return 'Text'

def get_website_info(url, headers, type):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title.string.strip() if soup.title else ''

        tags_to_extract = ['p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'strong', 'em', 'blockquote', 'cite', 'q', 'dfn', 'abbr', 'time', 'code', 'var', 'samp', 'kbd', 'sub', 'sup', 'i', 'b', 'u', 'mark', 'small', 'del', 'ins', 's']
        text_content = ' '.join([tag.get_text().strip() for tag in soup.find_all() if tag.name in tags_to_extract])

        description = soup.select_one('meta[name="description"]')['content'] if soup.select_one('meta[name="description"]') else ''
        keywords = soup.select_one('meta[name="keywords"]')['content'] if soup.select_one('meta[name="keywords"]') else ''

        if type == 'Video':
            youtube_id_match = re.search(r'youtube\.com/watch\?v=([^&]*)', url)
            youtube_short_id_match = re.search(r'youtu\.be/([^&]*)', url)
            if youtube_id_match:
                description = youtube_id_match.group(1)
            elif youtube_short_id_match:
                description = youtube_short_id_match.group(1)

        return {
            "title": title,
            "text_content": text_content,
            "description": description,
            "keywords": keywords
        }
    except Exception as e:
        print(f"Error when getting website info from {url}: {e}")
        return None

def add_to_crawl_list(url):
    with open("./crawl.txt", "a+", encoding='utf-8') as crawl_list:
        crawl_list.seek(0)
        lines = crawl_list.readlines()
        if any(url in line for line in lines):
            return "The request already exists in the list."
        
        try:
            result = urlparse(url)
            is_valid = all([result.scheme, result.netloc])
        except ValueError:
            is_valid = False

        if not is_valid:
            return "Your url is invalid."
        
        crawl_list.write(url + '\n')
    return "Your request has been successfully added to the list."

def load_to_deque():
    with open("./crawl.txt", 'r') as file:
        lines = file.readlines()
    return deque(lines)

def save_from_deque(d: deque):
    with open("./crawl.txt", 'w') as file:
        for line in d:
            file.write(line)

def ATMT(username, password):
    password = hashlib.md5(hashlib.sha256(password.encode('utf-8')).hexdigest().encode()).hexdigest()

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537.36'
    headers = {'User-Agent': user_agent}
    investigation_list = load_to_deque()
    checked_urls = set()

    while investigation_list:
        url = investigation_list.popleft()
        checked_urls.add(url)
        print("Investigating url: ", url)
        type = classify_website(url)
        website_info = get_website_info(url, headers, type)
        if website_info is not None:
            print("Title: ", website_info["title"])
            result = manager_insert_data(type, username, password, url, website_info["title"], website_info["text_content"], website_info["description"], website_info["keywords"], summarize_text(website_info["text_content"]))
            if result == "Content already exists in the database.":
                site_id = manager_get_id(type, url)
                print(manager_edit_data(type, username, password, site_id, url, website_info["title"], website_info["text_content"], website_info["description"], website_info["keywords"], summarize_text(website_info["text_content"])))
            else:
                print(result)
            print("---------")

            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = soup.select('a[href]')
            for link in search_results:
                new_url = urljoin(url, link.get('href'))
                if new_url not in investigation_list and new_url not in checked_urls:
                    investigation_list.append(new_url)
        else:
            site_id = manager_get_id(type, url)
            if site_id is not None:
                print(manager_remove_data(type, username, password, site_id))
    os.remove("./crawl.txt")
    save_from_deque(investigation_list)