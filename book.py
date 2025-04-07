import json
import requests
import mysql.connector
from mysql.connector import Error


def fetch_books(query, total_records):
    books = []
    page = 1
    while len(books) < total_records:
        url = f"https://openlibrary.org/search.json?q={query}&fields=title,author_name,isbn,publisher,first_publish_year,number_of_pages_median,cover_i&limit=100&page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for doc in data.get('docs', []):
                book = {
                    'title': doc.get('title'),
                    'author': ', '.join(doc.get('author_name', [])),
                    'isbn': doc.get('isbn', [None])[0],
                    'publisher': (doc.get('publisher', [])[0]),
                    'published_year': doc.get('first_publish_year'),
                    'pages': doc.get('number_of_pages_median'),
                    'image_url': f"https://covers.openlibrary.org/b/id/{doc.get('cover_i')}-L.jpg" if doc.get('cover_i') else None
                }

                if book['isbn'] and book not in books:
                    books.append(book)
                if len(books) >= total_records:
                    break
        else:
            print(f"Error fetching data: {response.status_code}")
            break
        page += 1
    return books


# Fetch 150 unique books related to 'fiction'
# books = fetch_books('fiction', 20)


# Step 1: Load existing JSON data
with open("bookdata.json", "r") as file:
    data = json.load(file)


# Step 2: Add new data
for i in data:
    if "booknumber" in i:
        del i["booknumber"]

 # If data is a list

# Step 3: Save updated data back
with open("bookdata.json", "w") as file:
    json.dump(data, file, indent=4)


# for i, j in enumerate(books):
#     print(i, j, end="\n\n")
