from django.db import models
from imdb import Cinemagoer

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster = models.CharField(max_length=500)

    def get_movie_data(self, id):
        return Cinemagoer.get_movie(id)