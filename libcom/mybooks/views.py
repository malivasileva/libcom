import requests

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from io import BytesIO
from PIL import Image, UnidentifiedImageError

from .models import Rating
from .models import User2Book
from .models import Status
from .forms import RatingForm

default_cover = '/static/images/no-cover.png'
def index(request):
    books = User2Book.objects.filter(user=request.user)
    read_list = []
    want_list = []
    complete_list = []

    for book in books:
        response = requests.get(f'{settings.GOOGLE_BOOKS_VOLUME}/{book.google_id}')
        jsonResponse = response.json()
        book_info = {'title': '', 'cover': ''}
        volumeInfo = jsonResponse.get('volumeInfo')
        book_info['title'] = volumeInfo.get('title', 'unknown')
        url = volumeInfo.get('imageLinks', default_cover)
        if (url != default_cover):
            url = url.get('thumbnail', default_cover)
        try:
            book_info['cover'] = url
            book_info['isbn'] = book.google_id

            if (book.status == Status.objects.get(status='Прочитано')):
                complete_list.append(book_info)

            if (book.status == Status.objects.get(status='Читаю')):
                read_list.append(book_info)

            if (book.status == Status.objects.get(status='Хочу прочитать')):
                want_list.append(book_info)

        except UnidentifiedImageError:
            print(f'{book.google_id} Не удалось идентифицировать изображение.')

    return render(request, 'mybooks/index.html', {'complete': complete_list, 'read': read_list, 'want': want_list})
def statistic(request):
    books = User2Book.objects.filter(user=request.user, status=Status.objects.get(status='Прочитано'))
    complete_list = []
    sumRating = 0
    authorName = ''

    for book in books:
        response = requests.get(f'{settings.GOOGLE_BOOKS_VOLUME}/{book.google_id}')

        if not response.ok:
            continue

        print(f'{settings.GOOGLE_BOOKS_VOLUME}/{book.google_id}')

        jsonResponse = response.json().get('volumeInfo')
        book_info = {'title': '', 'cover': '', 'number_of_pages': '', 'sum_rating': '', 'authors': ''}
        book_info['title'] = jsonResponse.get('title', '')
        book_info['number_of_pages'] = jsonResponse.get('pageCount', '')
        book_info['authors'] = jsonResponse.get('authors', [''])[0]

        # authors = jsonResponse.get('authors', '')
        # if (authors):
        #     author = requests.get(f"{settings.OPEN_LIBRARY_API_URL}{authors[0]['key']}.json")
        #     jsonAuthor = author.json()
        #     authorName = jsonAuthor.get('name', '')

        rating = Rating.objects.filter(user=request.user, isbn=book.google_id).first()
        if rating:
            sumRating = rating.general + rating.style + rating.characters + rating.plot
        book_info['sum_rating'] = sumRating

        url = jsonResponse.get('imageLinks', default_cover)
        if (url != default_cover):
            url = url.get('thumbnail', default_cover)

        #book_info['isbn'] = book.google_id
        book_info['cover'] = url

        # url = f'https://covers.openlibrary.org/b/isbn/{book.google_id}-M.jpg'
        # try:
        #     response = requests.get(url)
        #     img = Image.open(BytesIO(response.content))
        #     # Обработка изображения
        #     (width, height) = img.size
        #
        #     if (width <= 1 or height <= 1):
        #         book_info['cover'] = '/static/images/no-cover.png'
        #     else:
        #

        complete_list.append(book_info)

        # except UnidentifiedImageError:
        #     print(f'{book.google_id} Не удалось идентифицировать изображение.')

    def convert_to_int(s):
        try:
            return int(s)
        except ValueError:
            return 0

    max_pages_book = max(complete_list, key=lambda x: convert_to_int(x.get('number_of_pages', 0)))
    title_of_max_pages_book = max_pages_book['title']

    best_rating_book = max(complete_list, key=lambda x: convert_to_int(x.get('sum_rating', 0)))
    title_of_best_rating_book = best_rating_book['title']

    author_count = {}

    for book in complete_list:
        author_name = book['authors']
        if author_name in author_count:
            author_count[author_name] += 1
        else:
            author_count[author_name] = 1

    author_with_most_books = max(author_count.items(), key=lambda x: x[1])[0]

    return render(request, 'mybooks/statistic.html', {'complete': complete_list, 
                                                      'count_books': len(complete_list), 
                                                      'title_of_max_pages_book': title_of_max_pages_book,
                                                      'title_of_best_rating_book': title_of_best_rating_book,
                                                      'author': author_with_most_books,
                                                      'allAuthorsCount': author_count
                                                      })
def save_rating(request, isbn):
    if request.method == 'POST':
        general = request.POST.get('general')
        plot = request.POST.get('plot')
        characters = request.POST.get('characters')
        style = request.POST.get('style')
        review = request.POST.get('review')

        # Создаем или обновляем оценку
        ratings, created = Rating.objects.get_or_create(
            user=request.user,
            isbn=isbn,
            defaults={
                'general': general,
                'plot': plot,
                'characters': characters,
                'style': style,
                'review': review
            }
        )

        # Находим или создаем запись о книге пользователя
        user_book, created = User2Book.objects.get_or_create(
            user=request.user,
            google_id=isbn,
            defaults={'status': Status.objects.get(status='Прочитано')}
        )

        # Если запись не была создана, обновляем статус книги
        if not created:
            user_book.status = Status.objects.get(status='Прочитано')
            user_book.save()
    return HttpResponse('ok')
def save_read(request, isbn):
    if request.method == 'POST':
        # Находим или создаем запись о книге пользователя
        user_book, created = User2Book.objects.get_or_create(
            user=request.user,
            google_id=isbn,
            defaults={'status': Status.objects.get(status='Читаю')}
        )

        # Если запись не была создана, обновляем статус книги
        if not created:
            user_book.status = Status.objects.get(status='Читаю')
            user_book.save()
    return HttpResponse('ok')
def save_want(request, isbn):
    if request.method == 'POST':
        # Находим или создаем запись о книге пользователя
        user_book, created = User2Book.objects.get_or_create(
            user=request.user,
            google_id=isbn,
            defaults={'status': Status.objects.get(status='Хочу прочитать')}
        )

        # Если запись не была создана, обновляем статус книги
        if not created:
            user_book.status = Status.objects.get(status='Хочу прочитать')
            user_book.save()
    return HttpResponse('ok')
