import requests
from django.shortcuts import render
from django.conf import settings

def search_results_view(request, query):
    # Communicate with the Open Library API
    response = requests.get(f'{settings.OPEN_LIBRARY_API_URL}/search.json?q={query}')
    docs = response.json().get('docs', [])
    # , 'cover': ''
    books_info = []
    for doc in docs:
        book_info = {'title': '', 'authors': [], 'cover': ''}
        isbn = doc.get('isbn', [])
        book_info['authors'] = doc.get('author_name', [])
        book_info['title'] = doc.get('title', '')

        if isbn:
            book_info['cover'] = f'https://covers.openlibrary.org/b/isbn/{isbn[0]}-M.jpg'
        else:
            book_info['cover'] = '/static/images/no-cover.png'

        books_info.append(book_info)

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