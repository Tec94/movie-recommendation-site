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

import csv
from myapp.models import Movie

def import_books(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Movie.objects.create(
                userId=row['userId'],
                movieId=row['movieId'],
                rating=row['rating'],
                timestamp=row['timestamp']
            )

def index(request):
    algo = model_test.LoadPickel()
    csv_file_path = "C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\ratings.csv"  # Replace with your actual file path
    import_books(csv_file_path)
    print('after import')
    # get the recommended movies based on avengers movie id
    #recommended_movies = algo_test.predict_rating(algo, 1, model_test.getMovieId('Avengers'))
    print('check')

    return render(request, 'index.html', {})

def login(request):
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
    return render(request, 'login.html', {})