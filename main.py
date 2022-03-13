from flask import Flask, request
from flask import render_template

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login(): 
    if(request.method == 'POST'):
        # Retrieve data from form
        account_id = request.json['username']
        password = request.json['password']

        # Hash the password and compare to database

        # MySQL query : SELECT * FROM NURSE WHERE account_id={account_id}

        # return login
        return {'_code' : 'success'}

@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
