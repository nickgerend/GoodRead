# Written by: Nick Gerend, @dataoutsider
# Viz: "Good Read", enjoy!

import pandas as pd
import numpy as np
import requests 
import json
from urllib import parse
import time
import os

#books = pd.read_csv(os.path.dirname(__file__) + '/mostrecommendedbooks.csv')
#books = pd.read_csv(os.path.dirname(__file__) + '/thegreatestbooks.csv')
books = pd.read_csv(os.path.dirname(__file__) + '/1001bookreviews.csv')
query_books = books['title'].tolist()
query_authors = books['author'].tolist()

print(len(query_books))

def google_book_info(query_books, query_authors):
    book_info = []
    error_list = []
    not_found = []
    track = 1
    google_url = 'https://www.googleapis.com/books/v1/volumes?q=intitle:{}+inauthor:{}'
    for book, auth in zip(query_books, query_authors):
        try:
            url_split = list(parse.urlsplit(google_url.format(book,auth)))
            url_split[3] = parse.quote(url_split[3], safe='q=&')
            url = parse.urlunsplit(url_split)
            session = requests.Session()
            request = session.get(url=url)
            book_data = json.loads(request.text)
            selector = 0
            page_count = 0
            last_count = 0
            if "items" in book_data:
                for i in range(len(book_data["items"])):
                    volume_info = book_data["items"][i]
                    page_count = volume_info["volumeInfo"]["pageCount"] if "pageCount" in volume_info["volumeInfo"] else  np.nan
                    if i > 0:
                        if page_count > last_count:
                            selector = i
                    last_count = page_count
            if "items" in book_data:
                volume_info = book_data["items"][selector] 
                authors = volume_info["volumeInfo"]["authors"] if "authors" in volume_info["volumeInfo"] else  np.nan
                category = volume_info["volumeInfo"]["categories"] if "categories" in volume_info["volumeInfo"] else  np.nan
                pages = volume_info["volumeInfo"]["pageCount"] if "pageCount" in volume_info["volumeInfo"] else  np.nan
                publication_date = volume_info["volumeInfo"]["publishedDate"] if "publishedDate" in volume_info["volumeInfo"] else np.nan               
                book_info.append({"google_id": volume_info['id'],
                "title": volume_info["volumeInfo"]["title"],
                "author": authors, 
                "publication_date": publication_date,
                "category": category,
                "pages": pages})
            else: 
                not_found.append(book)
        except Exception as e:
            error_list.append(e)
        time.sleep(np.random.random())
        all_results = []
        all_results.append(book_info)
        all_results.append(error_list)
        all_results.append(not_found)
        print(track)
        track += 1
    df_found = pd.DataFrame(book_info, columns=['google_id', 'title', 'author', 'publication_date', 'category', 'pages'])
    return df_found, all_results

df_found, all_results = google_book_info(query_books, query_authors)
print(df_found)
df_found.to_csv(os.path.dirname(__file__) + '/1001bookreviews_google.csv', encoding='utf-8', index=False)
print('finished')