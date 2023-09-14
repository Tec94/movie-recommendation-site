from django.shortcuts import render
from .models import Movie
from imdb import Cinemagoer
import os

# Create your views here.
def url_clean(url):
    base, ext = os.path.splitext(url)
    i = url.count('@')
    s2 = url.split('@')[0]
    url = s2 + '@' * i + ext
    return url

def home(request):
    ia = Cinemagoer()
    ia.get_movie_infoset()
    movie = ia.search_movie("Matrix")
    movie = movie[0]
    url = url_clean(movie['cover url'])
    photo = url
    return render(request, 'home.html', {'movie': movie, 'photo': photo})
