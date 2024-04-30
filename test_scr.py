import csv, sqlite3

def import_mov():
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    with open('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\movies.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute('CREATE TABLE IF NOT EXISTS myapp_movies (movieId INTEGER, title TEXT, genres TEXT)')
            cur.execute('INSERT INTO myapp_movies (movieId, title, genres) VALUES (?, ?, ?)', row)
        cur.execute('DELETE FROM myapp_movies WHERE rowid = 1')

    con.commit()
    con.close()

def import_rat():
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    with open('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\ratings.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute('CREATE TABLE IF NOT EXISTS myapp_ratings (userId INTEGER, movieId INTEGER, rating REAL, timestamp INTEGER)')
            cur.execute('INSERT INTO myapp_ratings (userId, movieId, rating, timestamp) VALUES (?, ?, ?, ?)', row)
        cur.execute('DELETE FROM myapp_ratings WHERE rowid = 1')

    con.commit()
    con.close()

if __name__ == '__main__':
    import_mov()
    import_rat()