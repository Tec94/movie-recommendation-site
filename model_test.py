import pandas as pd, re, csv, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader, Dataset, SVD
import pickle as pi, sqlite3

model = None

def cleanTitle(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

def LoadFile():

    conn = sqlite3.connect('db.sqlite3')

    sql_query = '''
        SELECT userId, movieId, rating
        FROM myapp_ratings;
    '''

    ratings = pd.read_sql_query(sql_query, conn)

    
    sql_query = '''
        SELECT *
        FROM myapp_movies;
    '''

    movies = pd.read_sql_query(sql_query, conn)

    conn.close()

    movies["cleanTitle"] = movies["title"].apply(cleanTitle)

    return ratings, movies

ratings, movies = LoadFile()
user_ratings = ratings

def LoadFile2(ratings):
    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
    return data

def LoadPickel():
    global model
    if model == None:
        with open('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\algo.pkl', 'rb') as algo:
            model = algo.read()
    return model


def getMovieId(title):
    movieId = search(cleanTitle(title)).head(1)['movieId'].to_string(index=False)
    return movieId

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
    data = LoadFile2(ratings)
    algo = SVD()
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    pi.dumps(algo, open("C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\algo.pkl", "wb"))
