import requests
from django.shortcuts import render
from django.conf import settings

def search_results_view(request, query):
    # Communicate with the Open Library API
    response = requests.get(f'{settings.OPEN_LIBRARY_API_URL}/search.json?q={query}')
    docs = response.json().get('docs', [])
    #isbn_list = [doc.get('isbn', None) for doc in docs]
    #sbn_list = [isbn for isbn in isbn_list if isbn is not None]

    isbn_list = [isbn for doc in docs for isbn in doc.get('isbn', []) if isbn]

    isbn_list = isbn_list[:100]

    books_info = []

    #for isbn in isbn_list:
        # Make a request for each ISBN to obtain title and author information
        #book_info = get_book_info(isbn)
        #books_info.append(book_info)

    return render(request, 'search/index.html', {'results': books_info})


def get_book_info(isbn):
    # Make a request to get book information using ISBN
    book_info = {'isbn': isbn, 'title': '', 'authors': []}
    book_response = requests.get(f'{settings.OPEN_LIBRARY_API_URL}/isbn/{isbn}')

    #    if book_response.status_code == 200:
    #    book_data = book_response.json()
    #    book_info['title'] = book_data.get('title', '')
    #    authors = book_data.get('authors', [])
    #    for author in authors:
    #        author_key = author.get('key', '')
    #        # Make a request to get author information
    #        author_response = requests.get(f'{settings.OPEN_LIBRARY_API_URL}{author_key}.json')
    #        if author_response.status_code == 200:
    #            author_data = author_response.json()
    #            author_name = author_data.get('name', '')
    #            book_info['authors'].append(author_name)

    return book_response

def index(request):
    return render(request, 'search/index.html')

def search(request):
    response=requests.get('https://openlibrary.org/search.json?q=tolkien')