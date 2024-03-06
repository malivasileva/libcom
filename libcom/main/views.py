from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

def index(request):
    # if request.method == "POST":
    #     action = request.POST.get('action')
    #     if action == "login":
    #         username = request.POST.get('inputUsername')
    #         password = request.POST.get('inputPassword')
    #
    #         user = auth.authenticate(username=username, password=password)
    #
    #         if user is not None:
    #             auth.login(request, user)
    #             return redirect('home')
    #         else:
    #             messages.info(request, "Ivalid")
    #             return redirect('home')
    #
    #     elif action == "signup":
    #         first_name = request.POST.get('regFirstName')
    #         username = request.POST.get('regUsername')
    #         password1 = request.POST.get('password1')
    #         password2 = request.POST.get('password2')
    #         if password1 != password2:
    #             messages.info(request, "Пароли не совпадают")
    #             return redirect('home')
    #         else:
    #             if (User.objects.filter(username=username).exists()):
    #                 messages.info(request, "Пользователь с данным логином уже существует")
    #                 return redirect('home')
    #             else:
    #                 user = User.objects.create(username=username, first_name=first_name, password=password1)
    #                 user.save()

    return render(request, 'main/index.html')

def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('query')  # Assuming your search field is named 'query'
        if query:
            return redirect('search:search_results', query=query)
    return redirect('/')

def mybooks(request):
    return render(request, 'main/mybooks.html')

def about(request):
    return render(request, 'main/about.html')