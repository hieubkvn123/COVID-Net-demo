import hashlib
import sqlite3
import jwt
import datetime 
from functools import wraps
from flask import g, jsonify
from flask import Flask, request, flash
from flask import render_template, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = b'FYP-COVID-DEMO-2022'

DATABASE = './fyp.db'

# For getting sqlite database cursor
def make_dicts(cursor, row):
	return dict((cursor.description[idx][0], value)
				for idx, value in enumerate(row))

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)

	db.row_factory = make_dicts
	return db

# Decorator for protecting endpoints with JWT tokens
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.cookies.get("access_token")

		if(not token):
			return jsonify({'message' : 'Token is missing'}), 401

		try:
			data = jwt.decode(token, app.secret_key)
		except:
			return jsonify({'message' : 'Token is invalid'}), 401
		
		return f(*args, **kwargs)

	return decorated

# Get username from the token
def username_from_token(token):
	data = jwt.decode(token, app.secret_key)
	return data['username']

@app.route('/login', methods=['POST'])
def login(): 
	if(request.method == 'POST'):
		# Retrieve data from form
		account_id = request.form['username']
		password = request.form['password']

		# Hash the password 
		hash_password = hashlib.md5(password.encode()).hexdigest()

		# Query the database for account with same username 
		cursor = get_db().execute(f"SELECT * FROM ACCOUNT WHERE account_id='{account_id}'")
		rows = cursor.fetchall()
		cursor.close()

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
					'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
					key=app.secret_key)
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
