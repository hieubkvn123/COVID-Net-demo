import hashlib
import jwt
import datetime 
from flask import Flask, request, flash
from flask import render_template, redirect, url_for, make_response

# Import utilities
from utils.db import execute_query 
from utils.tokens import token_required, username_from_token, secret_key, timeout_mins

app = Flask(__name__)
app.secret_key = secret_key

@app.route('/login', methods=['POST'])
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
					key=app.secret_key)

				# Create a response and set access token as a cookie
				response = make_response(redirect(url_for('user_page')))
				response.set_cookie('access_token', token)
				return response

		# return invalid response if all of the above fails
		return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/', methods=['GET'])
def login_page():
	return render_template('login.html')


@app.route('/user', methods=['GET'])
@token_required
def user_page():
	token = request.cookies.get('access_token')
	username = username_from_token(token)
	return 'Welcome back ' + username

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=8080)
