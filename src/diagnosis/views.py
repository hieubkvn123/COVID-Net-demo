from flask import request, render_template

from src.entities.diagnosis import Diagnosis
from utils.tokens import token_required, username_from_token

class RecordsView:
    def __init__(self):
        super(RecordsView, self).__init__()
        self._entity_diagnosis = Diagnosis()

    @token_required
    def list_view(self):
        '''
            | @Route /records/list GET
            | @Access Private
            | @Desc : Retrieve all diagnosis records from the database and display list view. The following 
              information will be displayed : NRIC, patient's full name, date-time when diagnosis is recorded, 
              diagnosis result. Note, one patient may have multiple diagnosis.

            |
        '''
        print(request.data)
        token = request.cookies.get('access_token')
        username = username_from_token(token)

        # Get all records and return
        results = self._entity_diagnosis.list()
        if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400
        results = [
            {
                'nric_fin' : row['nric_fin'],
                'name' : ' '.join((row['fname'], row['lname'])),
                'date_time' : row['date_time'],
                'result' : row['result']
            } for row in results['payload']
        ]

        all_nric = [row['nric_fin'] for row in results]

        return render_template('user-list-records.html', **{'username' : username, 'records' : results, 'all_nric' : all_nric})

    @token_required
    def search_view(self):
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

    @token_required
    def update_view(self):
        token = request.cookies.get('access_token')
        username = username_from_token(token)

        return render_template('user-update-records.html', **{'username' : username})

    @token_required
    def create_view(self):
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