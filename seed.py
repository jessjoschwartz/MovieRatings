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
            title = title[0:-7]
            new_movie = model.Movie(id=row[0], name=title, released_at=dateobj, imdb_url=row[3])
            
            session.add(new_movie)


def load_ratings(session):
    # use u.data
    with open('seed_data/u.data', 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            new_rating = model.Rating(movie_id=row[1], rating=row[2], user_id=row[0])
            session.add(new_rating)
            


def main(session):
    # You'll call each of the load_* functions with the session as an argument
        load_users(session)
        load_movies(session)
        load_ratings(session)
        session.commit()  

if __name__ == "__main__":
    s= model.connect()
    main(s)
