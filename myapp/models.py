from django.db import models
from imdb import Cinemagoer

# Create your models here.
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return self.username
    
class Rating(models.Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    rating = models.CharField(max_length=255)  # changed from models.FloatField()
    timestamp = models.IntegerField()

    def __str__(self):
        return self.movieId
