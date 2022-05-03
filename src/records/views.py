from flask import render_template, request
from utils.tokens import token_required, username_from_token
from src.entities.patient_records import PatientRecords

class RecordView:
    def __init__(self):
        super(RecordView, self).__init__()
        self._entity_record = PatientRecords()

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

    @token_required
    def list_view(self):
        '''
            | @Route /records/list GET
            | @Access Private
            | @Desc : Display a tabular view of all the patient records.
        '''
        token = request.cookies.get('access_token')
        username = username_from_token(token)

        # Get all records and return
        results = self._entity_record.list()
        if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400
        results = [
            {
                'nric_fin' : row['nric_fin'],
                'name' : ' '.join((row['fname'], row['lname'])),
                'phone' : row['phone'],
                'gender' : row['gender'],
                'dob' : row['dob']
            } for row in results['payload']
        ]

        all_nric = [row['nric_fin'] for row in results]

        return render_template('user-list-records.html', **{'username' : username, 'records' : results, 'all_nric' : all_nric})
