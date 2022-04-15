from . import records_routes

from flask import request, render_template

from utils.tokens import token_required, username_from_token
from utils.db import execute_query

@records_routes.route('/list', methods=['GET'])
@token_required
def list_view():
    '''
        | @Route /records/list GET
        | @Access Private
        | @Desc : Retrieve all diagnosis records from the database and display list view. The following 
          information will be displayed : NRIC, patient's full name, date-time when diagnosis is recorded, 
          diagnosis result. Note, one patient may have multiple diagnosis.
        |
    '''
    
    token = request.cookies.get('access_token')
    username = username_from_token(token)

    # Get all records and return
    query = "SELECT d.patient_nric_fin, pr.fname || ' ' || pr.lname AS name, d.date_time, d.result FROM DIAGNOSIS d JOIN PATIENT_RECORD pr ON d.patient_nric_fin=pr.nric_fin ORDER BY d.date_time;"
    results = execute_query(query)

    all_nric = [row['patient_nric_fin'] for row in results]

    return render_template('user-list-records.html', **{'username' : username, 'records' : results, 'all_nric' : all_nric})

@records_routes.route('/search', methods=['GET'])
@token_required
def search_view():
    '''
        | @Route /records/search GET
        | @Access Private
        | @Desc : Display the advance search UI in case a patient's NRIC is not known, the diagnosis records of
          patient can be found by first name, last name, date diagnosed and diagnosis result.
        |
    '''

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
    '''
        | @Route /records/create GET
        | @Access Private
        | @Desc : Display the create record UI. The create record UI includes input fields for particulars like NRIC,
          first and last names, gender, date of birth, phone number and a image uploader.
        |
    '''

    token = request.cookies.get('access_token')
    username = username_from_token(token)

    return render_template('user-create-record.html', **{'username' : username})