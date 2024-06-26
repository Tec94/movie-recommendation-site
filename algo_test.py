# import everything from model_test.py
import model_test
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
from collections import defaultdict
import pickle as pi, re, pandas as pd
from datetime import time

# load the data
ratings, movies = model_test.LoadFile()
data = model_test.LoadFile2(ratings)
user_ratings = ratings

def predict_rating(algo, user_id, movie_id):
    # Load the data
    data = model_test.LoadFile2()

    # Add the user's past user_ratings to the data before building trainset
    user_ratings = pd.read_csv('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\user_ratings.csv')
    for index, row in user_ratings.iterrows():
        data.raw_ratings.append((row['userId'], row['movieId'], row['rating'], 0))

    # Train the SVD algorithm on the data
    algo = SVD()  # Initialize the SVD algorithm
    trainset = data.build_full_trainset()
    algo.fit(trainset)

    # Predict the rating for the movie
    prediction = algo.predict(user_id, movie_id)
    predicted_rating = prediction.est

    return predicted_rating

def getAccuracy():
    # Use the SVD algorithm
    algo = SVD()

    # Run 5-fold cross-validation and print results
    results = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=False)

    return results

def find_similar_movies(movie_id): # run for each movie then return a huge list of recommended movies
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]

