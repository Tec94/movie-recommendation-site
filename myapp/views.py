from django.shortcuts import render
from django.contrib import admin
from django.db import connections
from imdb import Cinemagoer
import imdb, os, random, pandas as pd, re, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

import model_test, algo_test

def getCoverUrl(movie_title):
    ia = imdb.IMDb()
    movies = ia.search_movie(movie_title)
    movie = movies[0]
    ia.update(movie)
    return movie['cover url']

def get_top_rated_movies(n=10):
    algo = model_test.LoadPickel()
    m = algo_test.get_top_movies(n)
    print(m)
    

def index(request):
    # algo = model_test.LoadPickel()
    # recommended_movies = algo_test.predict_rating(algo, 1, model_test.getMovieId('Avengers'))
    get_top_rated_movies()


    return render(request, 'index.html', {})

def login(request):
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
    return render(request, 'login.html', {})