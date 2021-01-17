# Written by: Nick Gerend, @dataoutsider
# Viz: "Good Read", enjoy!

import pandas as pd
import requests 
from bs4 import BeautifulSoup 
import os

#region Site 2: https://thegreatestbooks.org
def crawl(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    return soup

main_page = 'https://thegreatestbooks.org'
links = []

for i in range(54):
    link = main_page+'/?page='+str(i+1)
    links.append(link)
    
books = {}
for link in links:
    soup = crawl(link)
    titles = []
    authors = []
    for item in soup.find_all('div', {'class':'list-body'}):
        for tag in item.find_all('h4'):
            book = ''
            info = []
            for name in tag.find_all('a'):
                info.append(name.text)
            if len(info) == 2:
                book = info[0].strip() + ' - ' + info[1].strip()  
                books[book] = {}
                books[book]['title'] = info[0].strip()
                books[book]['author'] = info[1].strip()

df = pd.DataFrame.from_dict({(i): books[i] for i in books.keys() }, orient='index')
print(df)
#endregion

df.to_csv(os.path.dirname(__file__) + '/thegreatestbooks.csv', encoding='utf-8', index=False)