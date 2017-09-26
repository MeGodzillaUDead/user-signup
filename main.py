from flask import Flask, request, redirect, render_template
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True

# validation functions for different entry fields
# to be run from within the /welcome route 
# do these need to be available globally?
def validate_basic(entry):
	if len(entry) < 3:
		return "Must be longer than 3 characters."
	elif len(entry) > 20:
		return "Must be shorter than 20 characters."
	elif " " in entry:
		return "Cannot contain a space."
	else:
		return True
		
def validate_password(entry1, entry2):
	if validate_basic(entry1) == True:
		if entry1 != entry2:
			return "Passwords do not match."
		else:
			return True
	else:
		return validate_basic(entry1)
		
def validate_email(entry):
	if validate_basic(entry) == True:
		if ('@' in entry) and ('.' in entry):
			return True
		else:
			return "Not a valid e-mail address."
	else:
		return validate_basic(entry)

@app.route("/")
def index():
	return render_template('signup-form.html', title='New User Sign Up')

@app.route("/welcome", methods=['POST'])
def welcome():
	# get the data from the sign up form to perform validation
	user_name = request.form['user-name']
	pw = request.form['password']
	cpw = request.form['confirm-password']
	email = request.form['email']
	
	# get validation True or error message for each field
	uname_error = validate_basic(user_name)
	pw_error = validate_password(pw, cpw)
	if email == "":
		email_error = True
	else:
		email_error = validate_email(email)
	
	if uname_error == pw_error == email_error == True:
	# landing page render statement
		return render_template('welcome.html', title='Landing Page', name=user_name)
	else:
		return redirect("/?ue={0}&pe={1}&ee={2}".format(uname_error, pw_error, email_error))
		
app.run()
