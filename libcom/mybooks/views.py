from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Rating
from .models import User2Book
from .models import Status
from .forms import RatingForm

def index(request):
    return render(request, index)
def save_rating(request, isbn):
    if request.method == 'POST':
        general = request.POST.get('general')
        plot = request.POST.get('plot')
        characters = request.POST.get('characters')
        style = request.POST.get('style')
        review = request.POST.get('review_text')

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
            isbn=isbn,
            defaults={'status': Status.objects.get(status='Прочитано')}
        )

        # Если запись не была создана, обновляем статус книги
        if not created:
            user_book.status = Status.objects.get(status='Прочитано')
            user_book.save()
    return redirect('/')
