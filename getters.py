import requests
from bs4 import BeautifulSoup

import helpers

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_author(soup):
    author = soup.find("a", {"class": "nickname"})
    author = str(author)
    author = helpers.remove_tags(author)
    return author

def get_title(soup):
    title = soup.find("h1", {"class": "title"})
    title= str(title)
    title = helpers.remove_tags(title)
    return title

def get_max_page_number(soup):
    attributes_dictionary = soup.find("input", {"class": "inputText"}).attrs
    max_page_number = attributes_dictionary['max']
    max_page_number = int(max_page_number)
    return max_page_number

def get_chapter(soup):
    chapter_title = soup.find("h1", {"class": "subject"})
    chapter_title = str(chapter_title)
    chapter_title = helpers.remove_tags(chapter_title)
    return chapter_title

def get_text_body(soup):
    body = soup.find("div", {"class": "content -unselectable"})
    body = str(body)
    body = helpers.remove_tags(body)
    return body
