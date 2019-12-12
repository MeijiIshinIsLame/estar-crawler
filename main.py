import getters
import helpers
from crawler import *

import os

if __name__ == "__main__":

    path = input("Specify Path (if none leave blank): ")        
    url = input("Specify URL: ")
    
    soup = getters.get_soup(url)

    title = getters.get_title(soup)
    author = getters.get_author(soup)
    path = path + title
    
    try:
        os.remove(path + ".html")
    except OSError:
        pass

    book = Book(title, author, path)

    book.bind_book(url)
