from . import records_routes

from flask import request, render_template

from utils.tokens import token_required, username_from_token
from utils.db import execute_query

@records_routes.route('/list', methods=['GET'])
@token_required
def list_view():
    token = request.cookies.get('access_token')
    username = username_from_token(token)

    # Get all records and return
    query = "SELECT d.patient_nric_fin, pr.fname || ' ' || pr.lname AS name, d.date_time, d.result FROM DIAGNOSIS d JOIN PATIENT_RECORD pr ON d.patient_nric_fin=pr.nric_fin ORDER BY d.date_time;"
    results = execute_query(query)

    return render_template('user-list-records.html', **{'username' : username, 'records' : results})

@records_routes.route('/search', methods=['GET'])
@token_required
def search_view():
    token = request.cookies.get('access_token')
    username = username_from_token(token) 

    return render_template('user-search-records.html', **{'username' : username})

@records_routes.route('/update', methods=['GET'])
@token_required
def update_view():
    token = request.cookies.get('access_token')
    username = username_from_token(token)

    return render_template('user-update-records.html', **{'username' : username})

@records_routes.route('/create', methods=['GET'])
@token_required
def create_view():
    token = request.cookies.get('access_token')
    username = username_from_token(token)

    return render_template('user-create-record.html', **{'username' : username})