import model
import csv
import datetime

def load_users(session):
    # use u.user
    with open('seed_data/u.user', 'rb') as f:
        reader = csv.reader(f, delimiter='|', quoting=csv.QUOTE_NONE)
        for row in reader:
            # User.id=row[0]
            new_user = model.User(id=row[0], age=row[1], zipcode=row[4])
            session.add(new_user)
            session.commit()

def load_movies(session):
    # use u.item
     with open('seed_data/u.item', 'rb') as f:
        reader = csv.reader(f, delimiter='|', quoting=csv.QUOTE_NONE)
        for row in reader:
            title = row[1]
            title = title.decode("latin-1")
            if row[2] == "":
                dateobj = None
            else:
                dateobj = datetime.datetime.strptime(row[2], '%d-%b-%Y').date()
            new_movie = model.Movie(id=row[0], name=title, released_at=dateobj, imdb_url=row[3])
            movie_title = list(row[1])
            index = -7
            for letter in movie_title:
                while index < 0:
                    movie_title.pop(index)
                    index += 1
            movie_title = ''.join(movie_title)
            session.add(new_movie)
            session.commit()
            print row

def load_ratings(session):
    # use u.data
    with open('seed_data/u.data', 'rb') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in reader:
            new_rating = model.Rating(id=row[0], movie_id=row[1], rating=row[2], user_id=row[3])
            session.add(new_rating)
            session.commit()  


def main(session):
    # You'll call each of the load_* functions with the session as an argument
        load_users(session)
        load_movies(session)
        load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
