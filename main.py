from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login(request): 
    if(request.method == 'POST'):
        account_id = request.body['account_id']
        password = request.body['password']

        # MySQL query : SELECT * FROM NURSE WHERE account_id={account_id}

        # return login

@app.route('/', methods=['GET'])
def home(request):
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
