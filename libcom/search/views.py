from io import BytesIO

import requests
from django.shortcuts import render
from django.conf import settings
from PIL import Image, UnidentifiedImageError


def search_results_view(request, query):
    # Communicate with the Open Library API
    response = requests.get(f'{settings.OPEN_LIBRARY_API_URL}/search.json?q={query}')
    docs = response.json().get('docs', [])
    docs = docs[:30]
    books_info = []
    for doc in docs:
        book_info = {'title': '', 'authors': [], 'cover': '', 'isbn': ''}
        isbn = doc.get('isbn', [])
        book_info['authors'] = doc.get('author_name', [])
        book_info['title'] = doc.get('title', '')

        if isbn:
            url = f'https://covers.openlibrary.org/b/isbn/{isbn[0]}-M.jpg'

            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                # Обработка изображения
                (width, height) = img.size
                book_info['isbn'] = isbn[0]
                if (width <= 1 or height <= 1):
                    book_info['cover'] = '/static/images/no-cover.png'
                else:
                    book_info['cover'] = url
                books_info.append(book_info)

            except UnidentifiedImageError:
                print(f'{isbn[0]} Не удалось идентифицировать изображение.')

            #img = Image.open(requests.get(url, stream=True).raw)

        # else:
        #     book_info['cover'] = '/static/images/no-cover.png'
        #     book_info['isbn'] = ''
    return render(request, 'search/index.html', {'results': books_info})

def index(request):
    return render(request, 'search/index.html')

def search(request):
    response=requests.get('https://openlibrary.org/search.json?q=tolkien')