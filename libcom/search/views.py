from io import BytesIO

import requests
from django.shortcuts import render
from django.conf import settings
from PIL import Image, UnidentifiedImageError


def search_results_view(request, query):
    # Communicate with the Open Library API
    #response = requests.get(f'{settings.OPEN_LIBRARY_API_URL}/search.json?q={query}')
    response = requests.get(f'{settings.GOOGLE_BOOKS_SEARCH}q={query}')
    docs = response.json().get('items', [])
    docs = docs[:30]
    #log = docs[0].get('volumeInfo').get('imageLinks')
    log = []
    books_info = []

    for doc in docs:
        volumeInfo = doc.get('volumeInfo')
        title = volumeInfo.get('title')
        authors = volumeInfo.get('authors')
        cover = volumeInfo.get('imageLinks').get('thumbnail', '/static/images/no-cover.png')
        isbn = volumeInfo.get('industryIdentifiers')[0].get('identifier')
        #log.append(isbn)
        book_info = {'title': '', 'authors': [], 'cover': '', 'isbn': ''}
        book_info['authors'] = authors
        book_info['title'] = title
        book_info['cover'] = cover
        book_info['isbn'] = isbn
        books_info.append(book_info)

    return render(request, 'search/index.html', {'results': books_info})

        # if isbn:
        #     url = f'https://covers.openlibrary.org/b/isbn/{isbn[0]}-M.jpg'
        #
        #     try:
        #         response = requests.get(url)
        #         img = Image.open(BytesIO(response.content))
        #         # Обработка изображения
        #         (width, height) = img.size
        #         book_info['isbn'] = isbn[0]
        #         if (width <= 1 or height <= 1):
        #             book_info['cover'] = '/static/images/no-cover.png'
        #         else:
        #             book_info['cover'] = url
        #         books_info.append(book_info)
        #
        #     except UnidentifiedImageError:
        #         print(f'{isbn[0]} Не удалось идентифицировать изображение.')

        #img = Image.open(requests.get(url, stream=True).raw)

        # else:
        #     book_info['cover'] = '/static/images/no-cover.png'
        #     book_info['isbn'] = ''

def index(request):
    return render(request, 'search/index.html')

def search(request):
    response=requests.get('https://openlibrary.org/search.json?q=tolkien')