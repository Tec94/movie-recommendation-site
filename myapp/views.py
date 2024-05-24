from django.shortcuts import render
from django.contrib import admin
from django.db import connections
from imdb import Cinemagoer
import imdb, os, random, pandas as pd, re, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import threading
import model_test, algo_test

def getCoverUrl(movie_title):
    ia = imdb.IMDb()
    movies = ia.search_movie(movie_title)
    movie = movies[0]
    ia.update(movie)
    return movie['cover url']

def get_top_rated_movies(n=10):
    movies = algo_test.get_top_movies(n)
    return movies
    
def update_mv_list(username):
    pass


def index(request):
    threading.Thread(target=update_mv_list, args=[])

    m_list = algo_test.find_similar_movies(model_test.getMovieId('The Avengers'))
    print(m_list)
    movie_dict = []
    k = 0

    # for i in m_list:
    #     # print(m_list)
    #     try:
    #         print(getCoverUrl(i['title']))
    #     except:
    #         print("get URL function error")
    #     try:
    #         print(movie_dict[int(k)])
    #     except:
    #         print("movie_dict error")
    #     movie_dict[k] = getCoverUrl(i['title'])
    #     k += 1

    return render(request, 'index.html', {})
 
def login(request):
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
    return render(request, 'login.html', {})