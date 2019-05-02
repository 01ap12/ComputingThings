from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setDB import *
 
engine = create_engine('sqlite:///myDatabase.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()

# add 3 users to the db users
user = User("admin","12345")
session.add(user)
 
user = User("Mrs Ellis","1111")
session.add(user)
 
user = User("Dr Strange","2222")
session.add(user)
 
# commit the records to the database users
session.commit()
