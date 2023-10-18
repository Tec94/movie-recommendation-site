from django.shortcuts import render
from django.db import connections
from imdb import Cinemagoer
import imdb, os, random, pandas as pd, re, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

movies_rec = pd.read_csv('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\movies.csv')
ratings = pd.read_csv("C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\ratings.csv")
movies_rec["clean_title"] = movies_rec["title"].apply(clean_title)

vectorizer = TfidfVectorizer(ngram_range=(1,2))
tfidf = vectorizer.fit_transform(movies_rec["clean_title"])

def search(title):
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies_rec.iloc[indices].iloc[::-1]
    
    return results

# write a function that returns the movieId from the title using search function and only return the first result and the second id
def get_movie_id(title):
    movie_id = search(title).head(1)['movieId'].to_string(index=False)
    return movie_id

def find_similar_movies(movie_id):
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
    return rec_percentages.head(10).merge(movies_rec, left_index=True, right_on="movieId")[["score", "title", "genres"]]

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