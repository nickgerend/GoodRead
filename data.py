# Written by: Nick Gerend, @dataoutsider
# Viz: "Good Read", enjoy!

import pandas as pd
import numpy as np
import requests 
from bs4 import BeautifulSoup 
import re
import matplotlib.pyplot as plt
import os

#region Site 1: https://mostrecommendedbooks.com/best-books
def crawl(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    return soup

main_page = 'https://mostrecommendedbooks.com/best-books'
links = []
for tag in crawl(main_page).find_all('ul', {'class':'styles_sub-best-books__1VZwz'}):
    for attribute in tag.find_all('a'):
        element = attribute.get('href')
        link = element.replace(element, main_page+element[1:])
        links.append(link)
    
books = {}
for page in links:
    link = page.replace('-booksbest','')
    category_s = re.search('best-(.*)-books', link)
    category = category_s.group(1).replace('-', ' ')
    soup = crawl(link)
    titles = []
    authors = []
    for tag in soup.find_all('div', {'class':'styles_book-category-text__272Fl'}):
        book = ''
        for name in tag.find_all('h2'):           
            book = name.text      
            if book in books:
                books[book]['category'].append(category)
            else:
                books[book] = {}
                books[book]['category'] = [category]
                books[book]['title'] =  book
                for a in tag.find_all('h3'):
                    books[book]['author'] =  a.text
                    break
            break

df = pd.DataFrame.from_dict({(i): books[i] for i in books.keys() }, orient='index')
print(df)
df.to_csv(os.path.dirname(__file__) + '/mostrecommendedbooks.csv', encoding='utf-8', index=False)
#endregion

#region example
recommended_books = pd.read_csv(os.path.dirname(__file__) + '/most_recommended.csv', header=0, names=['recommender', 'title', 'author'])
recommended_books_reshaped = recommended_books.groupby(['title', 'author'])['recommender'].apply(lambda x: '|'.join(x)).reset_index()
recommended_books_reshaped['title'] = recommended_books_reshaped['title'].str.replace('"','')
query_books = recommended_books_reshaped['title'].tolist()
query_authors = recommended_books_reshaped['author'].tolist()
#endregion