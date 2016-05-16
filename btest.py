from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap 
from flask import Flask, request, jsonify, render_template

from wtforms import *
from wtforms.validators import *
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, StringField, SubmitField, validators

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

from datetime import date

app = Flask(__name__)
app.debug = True

Bootstrap(app)

engine = create_engine('sqlite:///final_database.db',echo=False)
Base = declarative_base()


Session= sessionmaker(bind=engine)
Session.configure()
session = Session()

class Classes(Base):
	__tablename__ = 'classes'
	id = Column(Integer, primary_key=True)
	classname = Column(String)
	professor = Column(String)
	location = Column(String)

#Unhash to add a table
#One to many relationship
#One class to many students

# class Students(Base):
# 	__tablename__ = 'students'
# 	id = Column(Integer, primary_key=True)
# 	student = Column(String)
# 	class_id = Column(Integer, ForeignKey('classes.id'))
# 	classname = relationship(Classes)

Base.metadata.create_all(engine)

results = session.query(Classes).all()
if len(results) == 0:

	#unhash for one to many relationship

	# class1 = Classes(classname='CS 330',professor='Miller',location='Olin')
	# class2 = Classes(classname='CS 353',professor='Miller',location='Olin')
	# class3 = Classes(classname='CS370',professor='Lee',location='Olin')
	# class4 = Classes(classname='ENG 212',professor='Lesmiester',location='Loyalty')
	# session.add(class1)
	# session.add(class2)
	# session.add(class3)
	# session.add(class4)
	# session.commit()

#unhash to generate student table information
#(one to many relationship with classes table)

# studentresults = session.query(Students).all()
# if len(results) == 0:
# 	student2 = Students(student='Andy Johnson', classname='CS 330')
# 	session.add(student2)
# 	student2 = Students(student='Connor Fitzpatrick', classname='CS 330')
# 	session.add(student2)
# 	student2 = Students(student='Connor Fitzpatrick', classname='CS 370')
# 	session.add(student2)
# 	student1 = Students(student='Connor Fitzpatrick', classname='CS 353')
# 	session.add(student1)
# 	student1 = Students(student='Connor Fitzpatrick', classname='ENG 212')
# 	session.add(student1)
# 	session.commit()


	school = Classes(classname='CS 330',professor='Miller', location='Olin')
	session.add(school)
	school = Classes(classname='CS 370',professor='Lee', location='Olin')
	session.add(school)
	school = Classes(classname='CS 353',professor='Miller', location='Olin')
	session.add(school)
	school = Classes(classname='ENG 212',professor='Lesmiester', location='Loyalty')
	session.add(school)
	session.commit()

@app.route('/classes/<int:school_id>')
def index(school_id):
	return jsonify(greeting="<h1>Hello Class Id # {}</h1>".format(school_id))

@app.route('/classes', methods=['GET'])
def get_all_schools():
	Session = sessionmaker(bind=engine)
	Session.configure()
	session=Session()
	results = session.query(Classes).all()
	reslist = []
	for row in results:
		reslist.append(dict(id=row.id,classname=row.classname,professor=row.professor,location=row.location))
	
	print(reslist)
	return jsonify(schoollist=reslist)

#unhash to generate students table

# @app.route('/students', methods=['GET'])
# def get_all_students():
# 	Session = sessionmaker(bind=engine)
# 	Session.configure()
# 	session=Session()
# 	studentresults = session.query(Classes).all()
# 	reslist = []
# 	for row in studentresults:
# 		print(row)
# 		reslist.append(dict(id=row.id,student=row.student,classname=row.classname))
	
# 	print(reslist)
# 	return jsonify(studentlist=reslist)

@app.route('/')
def hello_world():
	return render_template('bootstrap.html',foo='bar')

@app.route('/carousel')
def carousel():
	return render_template('carousel.html',foo='bar')

@app.route('/school')
def school():
	return render_template('finalAPI.html',foo='bar')

#unhash to feed html file with students table

# @app.route('/names')
# def names():
# 	return render_template('students.html',foo='bar')

class form_CreateUser(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password')

class form_SignIn(Form):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password')

#@login_manager.user_loader
#def load_user(user_id):
    #return User.get(user_id)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = form_CreateUser(csrf_enabled=False)
	if request.method == 'POST':
		print("in signup")
		formdata = request.form
		print("in signup2")
		firstname = formdata['firstname']
		lastname = formdata['lastname']
		email = formdata['email']
		password = formdata['password']

		#to add to a database:

		# if createUser(firstname, lastname, email, password):
		# 	#successful user
		# 	pass
		# else:
		# 	#failed user
		# 	pass

	return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = form_SignIn(csrf_enabled=False)
	if request.method == 'POST':
		formdata = request.form
		email = formdata['email']
		password = formdata['password']

		#to add to a database:

		# check = somedatabasename.session.query(User).filter_by(email=email).first()
		# if check.check_password(password):
		# 	login_user(check)
		# 	return redirect(url_for('hello'))

	return render_template('login.html', form=form)

#to add to a database:

# def createUser(fn, ln, em, pw):
#     # Adds a user to the database.
#     try:
#         me = User(fn, ln, em, pw)
#         somedatabasename.session.add(me)
#         somedatabasename.session.commit()
#         print("User created")
#         return True

#     except Exception as e:
#         # Prints why the user could not be added
#         print(e)
#         return False

if __name__ == '__main__':
	app.run()