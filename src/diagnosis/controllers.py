import os
import re
import datetime
import requests
from flask import request, url_for, redirect
from werkzeug.utils import secure_filename
from src.entities.patient_records import PatientRecords
from src.entities.diagnosis import Diagnosis

from utils.tokens import token_required, username_from_token
from config import IMG_UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from config import COMPUTING_SERVER_IP, COMPUTING_SERVER_PORT


class DiagnosisController:
    def __init__(self):
        super(DiagnosisController, self).__init__()
        self._entity_patient_record = PatientRecords()
        self._entity_diagnosis = Diagnosis()

    def allowed_file(self, filename):
        '''
            | @Route None
            | @Access None
            | @Desc : Checks if an image file's extension has the correct extension as listed in config.py.

            |
        '''
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def validate_nric(self, nric):
        '''
            | @Route None
            | @Access None
            | @Desc : Check the validity of the NRIC's format.
        '''
        nric_pattern = "^([A-Z]{1}[0-9]{7}[A-Z]{1})$"
        err_msg = ""

        if(not re.match(nric_pattern, nric)):
            err_msg += "NRIC must include an upper-case letter followed by 7 digits and another upper-case letter"

        return err_msg


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

    def make_prediction(self, folder, xray_image):
        '''
            | @Route None
            | @Access None
            | @Desc : An utility function that upload an X-Ray image to a folder in the upload directory then create the 
              diagnosis prediction result by making request to the computing server. The function returns the diagnosis 
              result, confidence, the X-Ray image's URL after uploaded and the date-time when prediction is made.
        '''
        
        # Create folder for patient
        patient_folder = os.path.join(IMG_UPLOAD_FOLDER, folder)
        if(not os.path.exists(patient_folder)):
            os.mkdir(patient_folder)

        # Store image
        if xray_image and self.allowed_file(xray_image.filename):
            print('[INFO] Image uploaded ... ')
            file_extension = xray_image.filename.split(".")[-1]
            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + f".{file_extension}"
            filename = secure_filename(filename)
            xray_image.save(os.path.join(IMG_UPLOAD_FOLDER, folder, filename))

        # Gather information to create record
        xray_img_url = f'/static/images/{folder}/{filename}'
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Post image to computing server for diagnosis
        url = f'http://{COMPUTING_SERVER_IP}:{COMPUTING_SERVER_PORT}/predict_single_image'
        with open(os.path.join(IMG_UPLOAD_FOLDER, folder, filename), 'rb') as f:
            files = {'xray' : f}
            res = requests.post(url, files=files)
            if(res.status_code != 200):
                return None, None, None, None

            payload = res.json()
        
        result = payload['_label']
        confidence = payload['_confidence']

        return result, confidence,xray_img_url, date_time

    @token_required
    def get_diagnosis(self):
        '''
            | @Route /diagnosis/get_diagnosis POST
            | @Access Private
            | @Desc : Get a diagnosis detail with patient's information (nric, name, ...) and diagnosis details (X-ray image, date-time diagnosed, ...)
              given the patient's NRIC and the date-time when the diagnosis is created.

            * Example input data for testing:

            .. code-block:: python
                
                import requests

                payload = { 'nric' : 'G123456N' }
                headers = { 'Content-Type' : 'application/json' }

                requests.post('https://host/diagnosis/get_diagnosis', json=payload, headers=headers)
        '''
        if(request.method == 'POST'):
            payload = request.get_json()
            nric = payload['nric']
            datetime = payload['datetime']

            results = self._entity_diagnosis.get_by_id_and_datetime(nric, datetime)
            if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400

            return {
                '_code' : 'success',
                'payload' : results['payload']
            }

    @token_required
    def delete_diagnosis(self):
        '''
            | @Route /diagnosis/delete_diagnosis POST
            | @Access Private
            | @Desc : Delete a particular diagnosis record given the patient's NRIC and date-time when the diagnosis is created.

            * Example input data for testing

            .. code-block:: python

                import requests

                payload = { 'nric' : 'G12345678N', 'date_time' : '2022-04-15 00:00:00' }
                headers = { 'Content-Type' : 'application/json' }

                requests.post('https://host/diagnosis/delete_diagnosis', json=payload, headers=headers)
        '''
        if(request.method == 'POST'):
            payload = request.get_json()
            nric = payload['nric']
            date_time = payload['datetime']

            results = self._entity_diagnosis.delete_by_key_and_datetime(nric, date_time)
            if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400

            return {
                '_code' : 'success',
                'payload' : None,
                'msg' : 'Record deleted successfully'
            }

    @token_required
    def create_diagnosis(self):
        '''
            | @Route /diagnosis/create_diagnosis POST
            | @Access Private
            | @Desc : This function runs in parallel with `records.controllers.create()`. After the patient record is recorded
              into the SQLite3 database, the uploaded x-ray image and the patient's NRIC will be forwarded to the computing server 
              for inference. The diagnosis result and diagnosis confidence will be returned to the client.

            * Example input data for testing:
            
            .. code-block:: python

                import requests

                files = {'xray' : open('path/to/file.png', 'rb')}
                payload = {'nric' : 'G123456N'}

                requests.post('https://host/diagnosis/create_diagnosis', data=payload, files=files)

            |
        '''
        
        if(request.method == 'POST'):
            # For retrieving staff's account id
            token = request.cookies.get('access_token')
            by_staff_id = username_from_token(token)

            xray_image = request.files['xray']
            nric = request.form['nric']

            # Make prediction
            result, confidence, xray_img_url, date_time = self.make_prediction(nric, xray_image)
            if(result is None) : return { '_code' : 'failed', 'msg' : 'Something is wrong with the connection to computing server' }, 400

            # Store diagnosis result
            results = self._entity_diagnosis.insert(nric, by_staff_id, date_time, result, confidence, xray_img_url)
            if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400

            
            return {
                '_code' : 'success',
                'msg' : 'Diagnosis recorded, file uploaded successfully ... ',
                'payload' : {
                    'result' : result,
                    'confidence' : f'{confidence*100:.2f}%'
                }
            }

    @token_required
    def create_existing_diagnosis(self):
        '''
            | @Route /diagnosis/create_existing_diagnosis POST
            | @Access Private
            | @Desc : This function is used to create diagnosis records for patients whose information already 
              exists in the system's database. If the NRIC's from the request's body does not exists, this function
              returns an error.

            * Example input data for testing:

            .. code-block:: python
                
                import requests

                files = {'xray' : open('path/to/file.png', 'rb')}
                payload = {'nric' : 'G123456N'}

                requests.post('https://host/diagnosis/create_existing_diagnosis', data=payload, files=files)
        '''

        if(request.method == 'POST'):
            # Get the NRIC from request body
            nric = request.form['nric']

            # Verify if the NRIC format is correct
            err_msg = self.validate_nric(nric)
            if(err_msg != ""):
                return {
                    '_code' : 'failed',
                    'msg' : err_msg
                }, 400

            # Verify if the NRIC exists in the database
            results = self._entity_patient_record.list_by_key(nric)
            if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400

            # If the record exists
            if(isinstance(results['payload'], list)):
                if(len(results['payload']) > 0):
                    return redirect(url_for('diagnosis.records_controllers_create_diagnosis'), code=307)
                else: # If the record does not exists
                    return {
                        '_code' : 'failed', 
                        'msg' : f'The patient record corresponding to {nric} does not exist'
                    }, 400


    @token_required
    def search_diagnosis(self):
        '''
            | @Route /diagnosis/search_diagnosis POST
            | @Access Private
            | @Desc : Used to search diagnosis records based on several attributes like nric/fin, first name, last name, ...

            * Example input data for testing:
            
            .. code-block:: python

                import requests

                headers = { 'Content-Type' : 'application/json' }
                payload = {'nric' : 'G123456N'}

                requests.post('https://host/diagnosis/search_diagnosis', json=payload, headers=headers)

            |
        '''

        if(request.method == 'POST'):
            payload = request.get_json()
            nric = payload['nric'] if 'nric' in payload else ""
            fname = payload['fname'] if 'fname' in payload else ""
            lname = payload['lname'] if 'lname' in payload else ""
            date = payload['date'] if 'date' in payload else ""
            result = payload['result'] if 'result' in payload else ""


            results = self._entity_diagnosis.search(nric, fname, lname, date, result)
            if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400

            return {
                '_code' : 'success',
                'payload' : results['payload']
            }

    @token_required 
    def create_batch_diagnosis(self):
        '''
            | @Route /diagnosis/create_batch_diagnosis POST
            | @Access Private
            | @Desc : Used to make multiple diagnosis using images named as existing patients' NRIC numbers.
        '''

        if(request.method == 'POST'):
            # For retrieving staff's account id
            token = request.cookies.get('access_token')
            by_staff_id = username_from_token(token)

            # Retrieve files from user's data form
            files = request.files
            payload = []
            
            for key, _file in files.items():
                filename = _file.filename 
                nric = filename.split('.')[0].split('_')[0]
                msg = 'Diagnosis created'
                result_code = 'success'

                # Check if the nric exists
                results = self._entity_patient_record.list_by_key(nric)
                if(results["_code"] == "query_error"): return { '_code' : 'failed', 'msg' : results['err_msg'] }, 400

                # If the record exists
                if(isinstance(results['payload'], list)):
                    if(len(results['payload']) < 1):
                        payload.append({
                            '_code' : 'failed',
                            'nric' : nric,
                            'result' : 'NONE',
                            'confidence' : 'NONE',
                            'xray_img_url' : 'NONE',
                            'msg' : 'Failed to retrieve patient info or patient does not exist'
                        })

                        continue

                # Make prediction
                result, confidence, xray_img_url, date_time = self.make_prediction(nric, _file)
                if(result is None):
                    result_code = 'failed'
                    msg = 'Connection to computing server experienced some problem'
                else:
                    # Store diagnosis result
                    results = self._entity_diagnosis.insert(nric, by_staff_id, date_time, result, confidence, xray_img_url)
                    if(results["_code"] == "query_error"): 
                        result_code = 'failed'
                        msg = 'Failed to store diagnosis result'

                result = {
                    '_code' : result_code,
                    'nric' : nric,
                    'result' : result,
                    'confidence' : confidence,
                    'xray_img_url' : xray_img_url,
                    'msg' : msg
                }

                payload.append(result)


            return {
                '_code' : 'success',
                'msg' : 'All images processed',
                'payload' : payload
            }

