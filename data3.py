# Written by: Nick Gerend, @dataoutsider
# Viz: "Good Read", enjoy!

import pandas as pd
import requests 
from bs4 import BeautifulSoup 
import os

#region Site 2: https://1001bookreviews.com/the-1001-book-list/
def crawl(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    return soup

main_page = 'https://1001bookreviews.com/the-1001-book-list/'

books = {}
soup = crawl(main_page)
titles = []
authors = []
complete = False
for item in soup.find_all('p'):
    #if '2000s' in item.text:
    elements = item.text.split('\n')
    for element in elements:
        if '–' in element:
            start = element.find('.')
            info = element[start+1:].split('–')
            if len(info) == 2:
                book = info[0].strip() + ' - ' + info[1].strip()  
                books[book] = {}
                books[book]['title'] = info[0].strip()
                books[book]['author'] = info[1].strip()
                if info[1].strip() == 'Aesopus':
                    complete = True
                    break
    if complete:
        break

df = pd.DataFrame.from_dict({(i): books[i] for i in books.keys() }, orient='index')
print(df)
#endregion

df.to_csv(os.path.dirname(__file__) + '/1001bookreviews.csv', encoding='utf-8', index=False)