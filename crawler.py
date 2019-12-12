from tqdm import tqdm
import time

import helpers
import getters

class Book:
    
    def __init__(self, title, author, path):
        self.title = title
        self.author = author
        self.path = path

    def create_title_page(self):

        title_with_tags = "<h1>" + self.title + "</h1>"
        author_with_tags = "<h2>" + self.author + "</h2>"

        title_page = title_with_tags + author_with_tags
        helpers.write_to_file(self.path, title_page)

    def create_content_page(self, current_page, chapter_title, body):

        current_page_formatted = "<br><br><b>" + str(current_page) + "</b><br><br>"
        helpers.write_to_file(self.path, current_page_formatted)

        if chapter_title != "None":
            chapter_title_formatted = "<h3>" + chapter_title + "</h3><br><br>"
            helpers.write_to_file(self.path, chapter_title_formatted)

        if body != "None":
            body_formatted = body.replace('\n', "<br>")
            helpers.write_to_file(self.path, body_formatted)

    def bind_book(self, url):

        soup = getters.get_soup(url)

        html_open = f"""

                    <html>

                    <head>

                    <title>{self.title} - {self.author}</title>
                             
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">

                    </head>
                    
                    <body>
                    <div class="container-fluid">
                      <div class="row">
                        <div class="col-sm-3">
                        </div>                  
                        <div class="col-sm-6">
                        <center>

                       """

        html_close = """
                        </center>
                        </div>
                        <div class="col-sm-6">
                        </div>
                      </div>
                    </div>
                </body>
            </html>
                    """

        #write initial html
        helpers.write_to_file(self.path, html_open)

        #write the title page
        self.create_title_page()

        current_page = 1
        page_url = url + "/viewer?page=" + str(current_page) #page 1
        soup = getters.get_soup(page_url)

        max_pages = getters.get_max_page_number(soup)
        
        #progress bar
        progress_bar = tqdm(total=max_pages)
        
        #traverse through all pages
        while(current_page <= max_pages):
            
            page_url = url + "/viewer?page=" + str(current_page)
            soup = getters.get_soup(page_url)

            chapter_title = getters.get_chapter(soup)
            body = getters.get_text_body(soup)

            self.create_content_page(current_page, chapter_title, body)

            current_page += 1

            #update progress bar
            progress_bar.update(1)
            time.sleep(1)

        progress_bar.close()
        helpers.write_to_file(self.path, html_close)
