from flask import Flask, request
from flask import render_template, redirect, url_for

# Import utilities
from utils.tokens import token_required, secret_key

# Include all the routers
from auth import auth_routes
from records import records_routes

app = Flask(__name__)
app.secret_key = secret_key

# Registering routes
app.register_blueprint(records_routes)
app.register_blueprint(auth_routes)

@app.route('/', methods=['GET'])
def login_page():
	'''
		| @Route / GET
		| @Access Public/Private
		| @Desc : First page to be seen by the users. The API will check if a JWT token exists
		  in the session. If the token exists, user will be redirected to user_main_page. Else, 
		  the login page will be rendered. 
		|
	'''
	token = request.cookies.get('access_token')
	if(token):
		return redirect(url_for('user_main_page'))
	return render_template('login.html')

@app.route('/user', methods=['GET'])
@token_required
def user_main_page():
	'''
		| @Route /user GET
		| @Access Private
		| @Desc : The first UI displayed when users are logged in.
		|
	'''
	
	# To be replaced with a real user main page later
	return redirect(url_for('records.create_view'))

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=8080)
