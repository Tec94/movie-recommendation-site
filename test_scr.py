import csv, sqlite3
from datetime import datetime

def import_mov():
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    with open('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\movies.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute('ALTER TABLE myapp_movie RENAME TO myapp_ratings')
            cur.execute('CREATE TABLE myapp_movies (movieId, title, genres)')

    con.commit()
    con.close()

if __name__ == '__main__':
    import_mov()