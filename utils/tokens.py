import jwt
from flask import jsonify, request, flash, redirect, url_for, make_response
from functools import wraps

secret_key = b'FYP-COVID-DEMO-2022'
timeout_mins = 60 # Expires after 1 hour

# Decorator for protecting endpoints with JWT tokens
def token_required(f):
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
	data = jwt.decode(token, secret_key)
	return data['username']