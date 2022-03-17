from distutils.util import execute
import sys 
from flask import Blueprint
from flask import request, jsonify

from utils.db import execute_query
from utils.tokens import token_required

records_routes = Blueprint("records", __name__, url_prefix="/records")

@records_routes.route("/create", methods=['POST'])
@token_required
def create():
    if(request.method == 'POST'):
        # Retrieve data from the payload
        payload = request.get_json()
        fname = payload['fname']
        lname = payload['lname']
        nric = payload['nric']
        gender = payload['gender']
        dob = payload['dob']
        phone = payload['phone']

        # Check if record already exists
        query = f"SELECT nric_fin FROM PATIENT_RECORD WHERE nric_fin='{nric}';"
        results = execute_query(query)

        if(isinstance(results, list)):
            if(len(results) > 0):
                print('[INFO] Record already exists ... ')
                return {'_code' : 'success'}

        # Record to the database
        # [INFO] NEED TO TAKE INTO ACCOUNT IMG URL LATER.
        query = f'INSERT INTO PATIENT_RECORD VALUES("{nric}", "{phone}", "{fname}", "{lname}", "{gender}", "{dob}", NULL);'
        results = execute_query(query, type="insert")

        if(results == "query_error"):
            print('Query error!')
            return {
                '_code' : 'failed',
                'msg' : 'Something wrong happened'
            }
        else: 
            return {
                '_code' : 'success'
            }