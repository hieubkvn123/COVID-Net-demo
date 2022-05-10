from lib2to3.pgen2 import token
import os
import re
import datetime
import requests
from flask import request
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

            xray_image = request.files['xray']
            nric = request.form['nric']

            # Create folder for patient
            patient_folder = os.path.join(IMG_UPLOAD_FOLDER, nric)
            if(not os.path.exists(patient_folder)):
                os.mkdir(patient_folder)

            # Store image
            if xray_image and self.allowed_file(xray_image.filename):
                print('[INFO] Image uploaded ... ')
                file_extension = xray_image.filename.split(".")[-1]
                filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + f".{file_extension}"
                filename = secure_filename(filename)
                xray_image.save(os.path.join(IMG_UPLOAD_FOLDER, nric, filename))

            # Gather information to create record
            xray_img_url = f'/static/images/{nric}/{filename}'
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            by_staff_id = username_from_token(token)

            # Post image to computing server for diagnosis
            url = f'http://{COMPUTING_SERVER_IP}:{COMPUTING_SERVER_PORT}/predict_single_image'
            with open(os.path.join(IMG_UPLOAD_FOLDER, nric, filename), 'rb') as f:
                files = {'xray' : f}
                res = requests.post(url, files=files).json()
            
            result = res['_label']
            confidence = res['_confidence']

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

