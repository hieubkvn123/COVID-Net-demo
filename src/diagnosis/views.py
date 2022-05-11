from flask import request, render_template

from src.entities.diagnosis import Diagnosis
from utils.tokens import token_required, username_from_token

class DiagnosisView:
    def __init__(self):
        super(DiagnosisView, self).__init__()
        self._entity_diagnosis = Diagnosis()

    @token_required
    def list_view(self):
        '''
            | @Route /diagnosis/list GET
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

        return render_template('user-list-diagnosis.html', **{'username' : username, 'records' : results, 'all_nric' : all_nric})

    @token_required
    def search_view(self):
        '''
            | @Route /diagnosis/search GET
            | @Access Private
            | @Desc : Display the advance search UI in case a patient's NRIC is not known, the diagnosis records of
              patient can be found by first name, last name, date diagnosed and diagnosis result.

            |
        '''

        token = request.cookies.get('access_token')
        username = username_from_token(token) 

        return render_template('user-search-diagnosis.html', **{'username' : username})

    @token_required
    def create_view(self):
        '''
            | @Route /diagnosis/create GET
            | @Access Private
            | @Desc : Display the create diagnosis for existing patient using their NRIC and X-Ray images.

            |
        '''

        token = request.cookies.get('access_token')
        username = username_from_token(token) 

        return render_template('user-create-diagnosis.html', **{'username' : username})
        