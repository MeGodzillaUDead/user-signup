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
		
'''def validate_password(entry1, entry2):
	if validate_basic(entry1) == True:
		if entry1 != entry2:
			return "Passwords do not match."
		else:
			return True
	else:
		return validate_basic(entry1)'''
		
def match(entry1, entry2):
	if entry1 == entry2:
		return True
	else:
		return "Passwords do not match."
		
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
	ue = request.args.get('ue')
	pe = request.args.get('pe')
	ee = request.args.get('ee')
	n_val = request.args.get('n_val')
	e_val = request.args.get('e_val')
	mc = request.args.get('mc')

# wtf doesn't this for loop work?!?!	
#	errors = [ue, pe, ee]
# 	for item in errors:
#		if item == None:
#			item = ""

	if ue == None:
		ue = ""
	if pe == None:
		pe = ""
	if ee == None:
		ee = ""
	if n_val == None or ue not in ["True", ""]:
		n_val = ""
	if e_val == None or ee not in ["True", ""]:
		e_val = ""
	if mc == None:
		mc = ""
	
	return render_template('signup-form.html', title='New User Sign Up',
		ue = ue,
		pe = pe,
		ee = ee,
		nv = n_val,
		ev = e_val,
		mc = mc
		)

@app.route("/welcome", methods=['POST'])
def welcome():
	# get the data from the sign up form to perform validation
	user_name = request.form['user-name']
	pw = request.form['password']
	cpw = request.form['confirm-password']
	email = request.form['email']
	
	# get validation True or error message for each field
	uname_error = validate_basic(user_name)
	pw_error = validate_basic(pw)
	match_check = match(pw, cpw)
	if email == "":
		email_error = True
	else:
		email_error = validate_email(email)
	
	if uname_error == pw_error == match_check == email_error == True:
	# landing page render statement
		return render_template('welcome.html', title='Landing Page', name=user_name)
	else:
		return redirect("/?ue={0}&pe={1}&ee={2}&n_val={3}&e_val={4}&mc={5}".format(uname_error, 
		pw_error, 
		email_error, 
		user_name, 
		email,
		match_check))
		
app.run()
