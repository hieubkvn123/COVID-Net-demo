import jwt
from flask import jsonify, request, flash, redirect, url_for, make_response
from functools import wraps
from config import SECRET_KEY, TOKEN_TIMEOUT

secret_key = SECRET_KEY
timeout_mins = TOKEN_TIMEOUT # Expires after 1 hour

# Decorator for protecting endpoints with JWT tokens
def token_required(f):
	'''
		| @Route None
		| @Access None
		| @Desc : A function wrapper used to verify the JWT token against the secret key. If the token is
		  valid, the corresponding API endpoint will be executed. In case the token is invalid or the token
		  is expired, the server will either return and error message or redirect user to home page.
	'''
	
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.cookies.get("access_token")

		if(not token):
			return jsonify({'message' : 'Token is missing'}), 401

		try:
			data = jwt.decode(token, secret_key)
		except jwt.ExpiredSignatureError:
			flash("Session expired", "info")
			response = make_response(redirect(url_for('login_page')))
			response.delete_cookie('access_token')

			return response
		except:
			return jsonify({'message' : 'Token is invalid'}), 401
		
		return f(*args, **kwargs)

	return decorated

# Get username from the token
def username_from_token(token):
	'''
		| @Route None
		| @Access None
		| @Desc : An utility function used to decode the username from token.
	'''

	data = jwt.decode(token, secret_key)
	return data['username']