from django.shortcuts import render
from django.db import connections
from .models import Movie
from imdb import Cinemagoer
import imdb
import os, random

# Create your views here.
def url_clean(url):
    base, ext = os.path.splitext(url)
    i = url.count('@')
    s2 = url.split('@')[0]
    url = s2 + '@' * i + ext
    return url

def home(request):
    ia = Cinemagoer('s3', 'mysql+mysqldb://root:root@localhost:3306/moviesDB') # local dataset - no cover url
    ib = imdb.IMDb() # imdb database - cover url
    ia.get_movie_infoset()
    ib.get_movie_infoset()

    movie1 = ia.get_movie(random.randint(0, 999999))
    movie2 = ia.get_movie(random.randint(0, 999999))
    movie3 = ia.get_movie(random.randint(0, 999999))
    movie4 = ia.get_movie(random.randint(0, 999999))
    movie5 = ia.get_movie(random.randint(0, 999999))
    movie6 = ia.get_movie(random.randint(0, 999999))

    # if keyerror raised then set a blank cover url
    try:
        mv1_cover = ib.search_movie(movie1['title'])[0].data['cover url']
    except KeyError:
        mv1_cover = ''
    try:
        mv2_cover = ib.search_movie(movie2['title'])[0].data['cover url']
    except KeyError:
        mv2_cover = ''
    try:
        mv3_cover = ib.search_movie(movie3['title'])[0].data['cover url']
    except KeyError:
        mv3_cover = ''
    try:
        mv4_cover = ib.search_movie(movie4['title'])[0].data['cover url']
    except KeyError:
        mv4_cover = ''
    try:
        mv5_cover = ib.search_movie(movie5['title'])[0].data['cover url']
    except KeyError:
        mv5_cover = ''
    try:
        mv6_cover = ib.search_movie(movie6['title'])[0].data['cover url']
    except KeyError:
        mv6_cover = ''

    url1 = url_clean(mv1_cover)
    url2 = url_clean(mv2_cover)
    url3 = url_clean(mv3_cover)
    url4 = url_clean(mv4_cover)
    url5 = url_clean(mv5_cover)
    url6 = url_clean(mv6_cover)

    photo1 = url1
    photo2 = url2
    photo3 = url3
    photo4 = url4
    photo5 = url5
    photo6 = url6

    return render(request, 'home.html', {'movie1': movie1, 'movie2': movie2, 'movie3': movie3, 'movie4': movie4, 'movie5': movie5, 'movie6': movie6, 'photo1': photo1, 'photo2': photo2, 'photo3': photo3, 'photo4': photo4, 'photo5': photo5, 'photo6': photo6})