from app import db

#First creating database
# db.create_all()
# db.session.commit()

#Deleting all data from database
db.delete_all()

#First create data base migration(when we we want to add new tables/columns to exciting database)