from flask import Flask
from sqlalchemy.orm import sessionmaker
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

# this will allow us to access the orm objects
from setDB import *

# creates database engine to database location
engine = create_engine('sqlite:///myDatabase.db', echo=True)

# creates an instance of Flask 
app = Flask(__name__)

# route decorator for the default path
@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:

		Session = sessionmaker(bind=engine)
		s = Session()

		users = s.query(User)


		return render_template("logged.html", users=users)
		#return "Welcome! " + str(request.form['username']).title() + " You are allowed! <br> <a href='/logout'>Logout</a>"

# route decorator for the login path
@app.route('/login', methods=['POST'])
def do_login():
	 
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])
	 
	Session = sessionmaker(bind=engine)
	s = Session()
	# query the db using the username and password posted
	# User object instance 
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	result = query.first()
	# the result is an object of type User
	if result:
		session['logged_in'] = True
	else:
		flash('wrong password!')

	session["username"] = POST_USERNAME

	if POST_USERNAME == "admin":
		session["admin"] = True
	else:
		session["admin"] = False

	return home()

@app.route('/logout')
def logout():
	if session['logged_in']:
		session['logged_in'] = False
		return home()

@app.route("/add", methods=['POST'])
def add():

	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])

	Session = sessionmaker(bind=engine)
	session = Session()

	user = User(POST_USERNAME,POST_PASSWORD)
	session.add(user)
	session.commit()

	return home()

@app.route("/remove", methods={"POST"})
def remove():
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])

	Session = sessionmaker(bind=engine)
	session = Session()


	query = session.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	remove = query.first()

	session.delete(remove)
	session.commit()
	return home()

@app.route("/edit", methods={"POST"})
def edit():
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])
	POST_NEWU = str(request.form["newU"])
	POST_NEWP = str(request.form["newP"])

	Session = sessionmaker(bind=engine)
	session = Session()


	query = session.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	edit = query.first()

	if POST_NEWP != "":
		edit.password = POST_NEWP 

	if POST_NEWU != "":
		edit.username = POST_NEWU

	session.commit()
	return home()


if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True, host='0.0.0.0', port=4000)