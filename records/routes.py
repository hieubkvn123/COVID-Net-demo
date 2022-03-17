from flask import Blueprint
from flask import request, jsonify

records_routes = Blueprint("records", __name__, url_prefix="/records")

@records_routes.route("/create", methods=['POST'])
def create():
    if(request.method == 'POST'):
        

        return {
            '_code' : 'success'
        }