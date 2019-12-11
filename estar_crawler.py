import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

#helpers
def remove_tags(soup):
    regex_pattern = re.compile('<.*?>')
    cleantext = re.sub(regex_pattern, '', soup)
    return cleantext

def remove_brackets(soup):
    regex_pattern = re.compile('\([^)]*\)')
    cleantext = re.sub(regex_pattern, '', soup)
    return cleantext

def write_to_file(title, content):
    file = title + ".html"
    with open(file, 'a') as f:
        f.write(content)

#main functions
def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_author(soup):
    author = soup.find("a", {"class": "nickname"})
    author = str(author)
    author = remove_tags(author)
    return author

def get_title(soup):
    title = soup.find("h1", {"class": "title"})
    title= str(title)
    title = remove_tags(title)
    return title

def get_max_page_number(soup):
    attributes_dictionary = soup.find("input", {"class": "inputText"}).attrs
    max_page_number = attributes_dictionary['max']
    max_page_number = int(max_page_number)
    return max_page_number

def get_chapter(soup):
    chapter_title = soup.find("h1", {"class": "subject"})
    chapter_title = str(chapter_title)
    chapter_title = remove_tags(chapter_title)
    return chapter_title

def get_text_body(soup):
    body = soup.find("div", {"class": "content -unselectable"})
    body = str(body)
    body = remove_tags(body)
    return body

def create_title_page(title, author):

    title_with_tags = "<h1>" + title + "</h1>"
    author_with_tags = "<h2>" + author + "</h2>"

    title_page = title_with_tags + author_with_tags
    write_to_file(title, title_page)

    return title_page

def create_content_page(title, current_page, chapter_title, body):

    current_page_formatted = "<b>" + str(current_page) + "</b><br><br>"
    write_to_file(title, current_page_formatted)

    if chapter_title != "None":
        chapter_title_formatted = "<h3>" + chapter_title + "</h3><br><br>"
        write_to_file(title, chapter_title_formatted)

    if body != "None":
        body_formatted = body.replace('\n', "<br>")
        write_to_file(title, body_formatted)

def bind_book(url):

    soup = get_soup(url)

    title = get_title(soup)
    author = get_author(soup)

    html_open = f"""

                <html>

                <head>

                <title>{title} - {author}</title>
                         
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">

                </head>
                
                <body>
                <div class="container-fluid">
                  <div class="row">
                    <div class="col-sm-3">
                    test
                    </div>                  
                    <div class="col-sm-6">
                    <center>

                   """

    html_close = """
                    </center>
                    </div>
                    <div class="col-sm-6">
                    test
                    </div>
                  </div>
                </div>
            </body>
        </html>
                """

    #write initial html
    write_to_file(title, html_open)

    #write the title page
    create_title_page(title, author)

    current_page = 1
    page_url = url + "/viewer?page=" + str(current_page)
    soup = get_soup(page_url)

    max_page_number = get_max_page_number(soup)

    progress_bar = tqdm(total=max_page_number)

    while(current_page <= max_page_number):
        page_url = url + "/viewer?page=" + str(current_page)
        soup = soup = get_soup(page_url)

        chapter_title = get_chapter(soup)
        body = get_text_body(soup)

        create_content_page(title, current_page, chapter_title, body)

        current_page += 1
        progress_bar.update(1)

    progress_bar.close()
    write_to_file(title, html_close)


url = "https://estar.jp/novels/17940303"

bind_book(url)
