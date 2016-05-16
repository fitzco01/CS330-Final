class form_CreateUser(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password')

class form_SignIn(Form):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password')



@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = form_CreateUser()
	if request.method == 'POST':
		print("in signup")
		formdata = request.form
		print("in signup2")
		firstname = formdata['firstname']
		lastname = formdata['lastname']
		email = formdata['email']
		password = formdata['password']

		if createUser(firstname, lastname, email, password):
			#user made successfully
			pass
		else:
			#make this return basic when we get there
			pass

	return render_template('newuser.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = form_SignIn()
	if request.method == 'POST':
		formdata = request.form
		email = formdata['email']
		password = formdata['password']
		check = db.session.query(User).filter_by(email=email).first()
		if check.check_password(password):
			login_user(check)
			return redirect(url_for('hello'))

	return render_template('login.html', form=form)