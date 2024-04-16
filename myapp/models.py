from django.db import models
from imdb import Cinemagoer

# Create your models here.
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return self.username

class Movie(models.Model):
    userId = models.IntegerField()
    movieId = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    timestamp = models.IntegerField()

    def __str__(self):
        return self.movieId
