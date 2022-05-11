import re

from flask import request 
from utils.tokens import token_required
from src.entities.patient_records import PatientRecords
from src.entities.diagnosis import Diagnosis

class RecordController:
    def __init__(self):
        super(RecordController, self).__init__()
        self._entity_patient_record = PatientRecords()
        self._entity_diagnosis = Diagnosis()

    def validate_input(self, fname, lname, nric, phone):
        '''
            | @Route None
            | @Access None
            | @Desc : Check the validity of user input for the create record endpoint. The following criterias will be applied on each
              input fields.

            * fname : Contains only letters (uppercase and lowercase) and some spacing.
            * lname : Contains only letters (uppercase and lowercase) and some spacing.
            * nric : One uppercase letter followed by 7 digits then another uppercase letter.
            * phone : Contains only digits.

            |
            
        '''
        err_msg = ""
        nric_pattern = "^([A-Z]{1}[0-9]{7}[A-Z]{1})$"
        name_pattern = "^[a-zA-Z ]+$"
        phon_pattern = "^[0-9]+$"

        if(not re.match(nric_pattern, nric)):
            err_msg += "NRIC must include an upper-case letter followed by 7 digits and another upper-case letter"

        if(not re.match(name_pattern, fname) or not re.match(name_pattern, lname)):
            if(err_msg != "") : err_msg += ", "
            err_msg += "Name must include only letter from a-z or A-Z with spacing"
        

        if(not re.match(phon_pattern, phone)):
            if(err_msg != "") : err_msg += ", "
            err_msg += "Phone number must include only digits"

        return err_msg


    @token_required
    def create_record(self):
        '''
            | @Route /records/create_record POST
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

    @token_required
    def get_record(self):
        '''
            | @Route /records/get_record
            | @Access Private
            | @Desc : Get information of a patient record given a particular patient's NRIC/FIN.
            
            * Example input data for testing:

            .. code-block:: python

                import requests

                payload = {
                    'nric' : 'G1234567N'
                }

                headers = { 'Content-Type' : 'application/json' }
                requests.post('https://host/records/get_record', json=payload, headers=headers)
        '''
        if(request.method == 'POST'):
            nric = request.get_json()['nric']

            # Get the record given the NRIC
            results = self._entity_patient_record.list_by_key(nric)
            if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400

            return {
                '_code' : 'success',
                'payload' : results['payload']
            }

    @token_required
    def update_record(self):
        '''
            | @Route /records/update_record POST
            | @Access Private
            | @Desc : Update a diagnosis records given the following information : nric, fname, lname, phone, gender, dob (PATIENT_RECORD table) and
              date-time when diagnosis is created (from DIAGNOSIS). The following cases will be included,
            
            * 1. NRIC is not modified : When the nurse did not mistake the NRIC of the patient but some of the basic particulars are wrong, the patient
              record attached to this NRIC will be updated with the new particular.
            * 2. NRIC is modified : When nurses mistook the NRIC of a patient with another, the following cases will be included
                * 2.1. The correct NRIC is already in the database : Update the basic particulars if modified and attach the diagnosis result to the 
                  correct NRIC.
                * 2.2. The correct NRIC is not inside the database : Create a new patient record with the particulars and the correct NRIC and attach
                  the diagnosis result to the correct NRIC.

        
            * Example input data for testing:
            
            .. code-block:: python
                
                import requests

                payload = { 
                    'nric' : 'G1778418N',
                    'fname' : 'Hieu',
                    'lname' : 'Nong',
                    'phone' : '88720435',
                    'dob' : '2000-04-30',
                    'gender' : 'Male',
                    'old_nric' : 'G1778418G' # Typo
                }
                headers = { 'Content-Type' : 'application/json' }
                requests.post('https://host/update_record/update_record', json=payload, headers=headers)

        '''
        if(request.method == 'POST'):
            payload = request.get_json()

            nric = payload['nric'].strip()
            fname = payload['fname']
            lname = payload['lname']
            phone = payload['phone']
            dob = payload['dob']
            gender = payload['gender']

            # Check the validity of the input
            validation_err_msg = self.validate_input(fname, lname, nric, phone)
            if(validation_err_msg != ""):
                return {
                    '_code' : 'failed',
                    'msg' : validation_err_msg
                }, 400


            # Update the basic particulars
            results = self._entity_patient_record.update_by_key(nric, {
                'fname' : fname,
                'lname' : lname,
                'phone' : phone,
                'dob' : dob,
                'gender' : gender
            })
            if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400

            return {
                '_code' : 'success',
                'payload' : None,
                'msg' : 'Record updated successfully'
            }

    @token_required
    def delete_record(self):
        '''
            | @Route /records/delete_record POST
            | @Access Private
            | @Desc : Delete patient's record by their NRIC/FIN.
        '''

        if(request.method == 'POST'):
            nric = request.get_json()['nric']
            results = self._entity_patient_record.delete_by_key(nric)
            if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400

            return {
                '_code' : 'success',
                'msg' : 'Patient record deleted successfully'
            }