import hashlib
import jwt
import datetime

from flask import current_app
from flask import request, flash, redirect, url_for, make_response
from utils.tokens import timeout_mins

from src.entities.account import Account

class AuthController:
	def __init__(self):
		super(AuthController, self).__init__()
		self._entity_account = Account()

	def login(self):
		'''
			| @Route /auth/login POST
			| @Access Public
			| @Desc : Login function. After the user filling in the username, password and submit the login form. 
			  The system checks if the particulars exist in the database and whether the password is correct. If
			  the credentials are valid, a JWT token will be generated and sent back to the client's session.

			* Example data for testing:

			.. code-block:: python

				import requests

				payload = {
					'username' : 'nong003',
					'password' : 'qazwsx007'
				}
				
				requests.post('http://host/auth/login', data=payload)
		'''

		if(request.method == 'POST'):
			# Retrieve data from form
			account_id = request.form['username']
			password = request.form['password']

			# Hash the password
			hash_password = hashlib.md5(password.encode()).hexdigest()

			# Query the database for account with same username
			rows = self._entity_account.list_by_key(account_id)['payload']

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

	def logout(self):
		'''
			| @Route /auth/login GET
			| @Access Public
			| @Desc : Once user pressed 'Logout', the system will clear the JWT token and redirect user to login page.
		'''
		response = make_response(redirect(url_for('login_page')))
		response.delete_cookie('access_token')

		return response