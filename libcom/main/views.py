from django.shortcuts import render, redirect


def index(request):
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