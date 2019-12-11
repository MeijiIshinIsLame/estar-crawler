import re
import os

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

def check_for_file(path):
    return os.path.isdir(path)
