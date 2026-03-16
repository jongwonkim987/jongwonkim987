"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, Http404
from django.shortcuts import render

premier_league = [
    {'team': 'Arsenal', 'manager': 'Arteta'},
    {'team': 'Man city', 'manager': 'Pep'},
    {'team': 'Man utd', 'manager': 'Carrick'},
    {'team': 'Aston villa', 'manager': 'Emery'},
]
def index(request):
    return HttpResponse("<h1>Hello, world.</h1>")

def book_list(request):
    book_text = ''

    return render(request, 'book_list.html', {'range': range(10)})

def book(request, num):
    book_text = ''
    return render(request, template_name='book_detail.html', context={'num': num})

def language(request, lang):
    return HttpResponse(f"<h1>{lang} 언어 페이지입니다.</h1>")

def python(request):
    return HttpResponse('python 페이지 입니다.')

def league(request):
    #league_title = [f'<a href="/league/{index}/">{league["team"]}</a>'
    #                for index, league in enumerate(premier_league)
    #                ]
    #response_text = '<br>'.join(league_title)

    return render(request, template_name='premier_league.html', context={'premier_league': premier_league})

def league_detail(request, index):
    if index > len(premier_league) - 1:
        raise Http404

    league = premier_league[index]
    context = {'league': league}
    return render(request, template_name='premier_leagues.html', context=context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('book_list/', book_list),
    path('book_list/<int:num>/', book),
    path('language/<str:lang>/', language),
    path('language/python/', python),
    path('league/', league),
    path('league/<int:index>/', league_detail),
]
