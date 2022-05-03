import re

from flask import request 
from utils.tokens import token_required
from src.entities.patient_records import PatientRecords

class RecordController:
    def __init__(self):
        super(RecordController, self).__init__()
        self._entity_patient_record = PatientRecords()

    def validate_input(self, fname, lname, nric, phone):
        '''
            | @Route None
            | @Access None
            | @Desc : Check the validity of user input for the create record endpoint. The following criterias will be applied on each
              input fields.

            * fname : Contains only letters (uppercase and lowercase).
            * lname : Contains only letters (uppercase and lowercase).
            * nric : One uppercase letter followed by 7 digits then another uppercase letter.
            * phone : Contains only digits.

            |
            
        '''
        err_msg = ""
        nric_pattern = "^([A-Z]{1}[0-9]{7}[A-Z]{1})$"
        name_pattern = "^[a-zA-Z]+$"
        phon_pattern = "^[0-9]+$"

        if(not re.match(nric_pattern, nric)):
            err_msg += "NRIC must include an upper-case letter followed by 7 digits and another upper-case letter"

        if(not re.match(name_pattern, fname) or not re.match(name_pattern, lname)):
            if(err_msg != "") : err_msg += ", "
            err_msg += "Name must include only letter from a-z or A-Z"
        

        if(not re.match(phon_pattern, phone)):
            if(err_msg != "") : err_msg += ", "
            err_msg += "Phone number must include only digits"

        return err_msg


    @token_required
    def create(self):
        '''
            | @Route /records/create POST
            | @Access Private
            | @Desc : The controller for creating a record. The create record form data will be received and will be recorded into the 
              SQLite3 database once verified.
            
            * Example input data for testing:

            .. code-block:: python

                import requests

                payload = {
                    'fname' : 'John',
                    'lname' : 'Doe',
                    'nric' : 'G1234567N',
                    'gender' : 'Male',
                    'dob' : '1998-01-01',
                    'phone' : '12345678'
                }

                headers = { 'Content-Type' : 'application/json' }
                requests.post('https://host/records/create', json=payload, headers=headers)
                
            |  
        '''

        if(request.method == 'POST'):
            # Retrieve data from the payload
            payload = request.get_json()
            fname = payload['fname']
            lname = payload['lname']
            nric = payload['nric']
            gender = payload['gender']
            dob = payload['dob']
            phone = payload['phone']

            # Check the validity of the input
            validation_err_msg = self.validate_input(fname, lname, nric, phone)
            if(validation_err_msg != ""):
                return {
                    '_code' : 'failed',
                    'msg' : validation_err_msg
                }, 400

            # Check if record already exists
            results = self._entity_patient_record.list_by_key(nric)
            if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400

            # If the record exists
            if(isinstance(results['payload'], list)):
                if(len(results['payload']) > 0):
                    return {
                        '_code' : 'failed',
                        'payload' : None,
                        'msg' : f'''Record with NRIC/FIN {nric} already exists. Please go to "Create Diagnosis" tab to create a new diagnosis for patient with NRIC/FIN of {nric}.'''
                    }, 400

            # If not exist, Record to the database
            results = self._entity_patient_record.insert(nric, fname, lname, dob, gender, phone)
            if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400

            return {
                '_code' : 'success',
                'payload' : None,
                'msg' : 'Record created successfully'
            }