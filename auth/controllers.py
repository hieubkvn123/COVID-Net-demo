from . import auth_routes

import hashlib
import jwt
import datetime

from flask import current_app
from flask import request, flash, redirect, url_for, make_response
from utils.tokens import timeout_mins

from utils.db import execute_query

@auth_routes.route('/login', methods=['POST'])
def login():
	if(request.method == 'POST'):
		# Retrieve data from form
		account_id = request.form['username']
		password = request.form['password']

		# Hash the password
		hash_password = hashlib.md5(password.encode()).hexdigest()

		# Query the database for account with same username
		rows = execute_query(f"SELECT * FROM ACCOUNT WHERE account_id='{account_id}'")

		# If length of results < 1 - invalid
		if(len(rows) < 1):
			flash("Invalid username. Please try again", "danger")
			return redirect(url_for('login_page'))
		else: # If username exists
			real_password = rows[0]['password']
			if(real_password != hash_password):
				flash("Invalid password. Please try again", "danger")
				return redirect(url_for("login_page"))
			else: # Correct password and username
				# Generate a JWT token
				token = jwt.encode({'username' : account_id,
					'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout_mins)},
					key=current_app.secret_key)

				# Create a response and set access token as a cookie
				response = make_response(redirect(url_for('user_main_page')))
				response.set_cookie('access_token', token)
				return response

		# return invalid response if all of the above fails
		return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@auth_routes.route('/logout')
def logout():
	response = make_response(redirect(url_for('login_page')))
	response.delete_cookie('access_token')

	return response