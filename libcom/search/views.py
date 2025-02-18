from io import BytesIO

import requests
from django.shortcuts import render
from django.conf import settings
from PIL import Image, UnidentifiedImageError


def search_results_view(request, query):
    # Communicate with the Open Library API
    #response = requests.get(f'{settings.OPEN_LIBRARY_API_URL}/search.json?q={query}')
    default_cover = '/static/images/no-cover.png'
    log = []
    response = requests.get(f'{settings.GOOGLE_BOOKS_SEARCH}q={query}?key={settings.GOOGLE_API_KEY}')
    items = response.json().get('items', [])
    items = items[:30]
    books_info = []

    for item in items:
        volumeInfo = item.get('volumeInfo')
        title = volumeInfo.get('title')
        authors = volumeInfo.get('authors')
        cover = volumeInfo.get('imageLinks', default_cover)
        if (cover != default_cover):
            cover = cover.get('thumbnail', default_cover)
        log.append(cover)
        id = item.get('id', '0')
        #isbn = volumeInfo.get('industryIdentifiers')[0].get('identifier')
        book_info = {'title': '', 'authors': [], 'cover': '', 'isbn': ''}
        book_info['authors'] = authors
        book_info['title'] = title
        book_info['cover'] = cover
        book_info['isbn'] = id
        books_info.append(book_info)

    return render(request, 'search/index.html', {'results': books_info})

def index(request):
    return render(request, 'search/index.html')

def search(request):
    response=requests.get('https://openlibrary.org/search.json?q=tolkien')