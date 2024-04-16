
import pandas as pd
import re
import csv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader, Dataset, SVD
import pickle as pi


def LoadFile():
    # Load the dataset
    ratings = pd.read_csv("C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\ratings.csv")
    movies = pd.read_csv('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\movies.csv')
    movies["cleanTitle"] = movies["title"].apply(cleanTitle)

    # Define the format
    reader = Reader(rating_scale=(0, 5))

    # Load the data from the file using the reader format
    return Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

def LoadPickel():
    with open('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\algo.pkl', 'rb') as algo:
        algo_content = algo.read()
    return algo_content


def cleanTitle(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

movies = pd.read_csv('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\movies.csv')
movies["cleanTitle"] = movies["title"].apply(cleanTitle)

def getMovieId(title):
    movieId = search(cleanTitle(title)).head(1)['movieId'].to_string(index=False)
    return movies[movies['title'] == title]['movieId'].to_string(index=False)

def search(title):
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    tfidf = vectorizer.fit_transform(movies["cleanTitle"])
    title = cleanTitle(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]
    
    return results

def addRating(userId, movieName, rating):

    # get the movieId of movieName
    movieId = search(movieName).head(1)['movieId'].to_string(index=False)

    if movieId is None:
        return

    # save the rating to new csv called user_ratings.csv
    with open('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\ratings.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([userId, movieId, rating, 0])


def TrainModel():
    data = LoadFile()
    algo = SVD()
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    pi.dumps(algo, open("C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\algo.pkl", "wb"))

def updateUserPredictions(uid):
    # get the user's past user_ratings
    user_ratings = pd.read_csv('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\user_ratings.csv')

    # add the user's past user_ratings to the data before building trainset
    for index, row in user_ratings.iterrows():
        data.raw_ratings.append((row['userId'], row['movieId'], row['rating'], 0))

    # predict the rating for the movie
    prediction = algo.predict(uid, movie_id)
    predicted_rating = prediction.est

    return predicted_rating