from flask import Flask, request
from flask import redirect, url_for

# Import utilities
from utils.tokens import secret_key

# Include all the routers
from src.auth import auth_routes
from src.diagnosis import diagnosis_routes
from src.records import records_routes

# Some config variables
from config import DEFAULT_ROUTE_AUTHENTICATED, DEFAULT_ROUTE_GUESS

app = Flask(__name__)
app.secret_key = secret_key

# Registering routes
app.register_blueprint(diagnosis_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(records_routes)

# Default routing
@app.route('/', methods=['GET'])
def default_route():
	'''
		| @Route /user GET
		| @Access Private
		| @Desc : The first UI displayed when users are logged in. For guess users, it will be
		  the login page. For authenticated user, it will be the create diagnosis and patient 
		  record page.
		|
	'''
	
	token = request.cookies.get('access_token')
	if(token):
		return redirect(url_for(DEFAULT_ROUTE_AUTHENTICATED))
	else:
		return redirect(url_for(DEFAULT_ROUTE_GUESS))

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=8080)
