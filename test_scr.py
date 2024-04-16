import csv, sqlite3
from datetime import datetime
from myapp.models import Movie

def import_mov():
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    with open('C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\ratings.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute('INSERT INTO myapp_movie (userId, movieId, rating, timestamp) VALUES (?, ?, ?, ?)', row)

    con.commit()
    con.close()

if __name__ == '__main__':
    csv_file_path = "C:\\Users\\user\\Desktop\\New folder\\code\\movie-recommendation-site\\ml-25m\\ratings.csv"  # Replace with your actual file path
    import_mov()