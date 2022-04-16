import os
import datetime
import requests
from flask import request
from werkzeug.utils import secure_filename

from utils.db import execute_query
from utils.tokens import token_required, username_from_token
from config import IMG_UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from config import COMPUTING_SERVER_IP, COMPUTING_SERVER_PORT


class RecordsController:
    def __init__(self):
        super(RecordsController, self).__init__()

    def allowed_file(self, filename):
        '''
            | @Route None
            | @Access None
            | @Desc : Checks if an image file's extension has the correct extension as listed
            in config.py. 
            |
        '''
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

            # Check if record already exists
            query = f"SELECT nric_fin FROM PATIENT_RECORD WHERE nric_fin='{nric}';"
            results = execute_query(query)

            if(isinstance(results, list)):
                if(len(results) > 0):
                    # Update all particulars
                    query = f'UPDATE PATIENT_RECORD SET fname="{fname}", lname="{lname}", gender="{gender}", dob="{dob}", phone="{phone}" WHERE nric_fin="{nric}";'
                    results = execute_query(query, type="update")

                    return {
                        '_code' : 'success',
                        'msg' : "Patient's NRIC already exists, Updating diagnosis result and X-Ray ... "
                    }

            # Record to the database
            query = f'INSERT INTO PATIENT_RECORD VALUES("{nric}", "{phone}", "{fname}", "{lname}", "{gender}", "{dob}");'
            results = execute_query(query, type="insert")

            if(results == "query_error"):
                return {
                    '_code' : 'failed',
                    'msg' : 'Something wrong happened'
                }
            else:
                return {
                    '_code' : 'success',
                    'msg' : 'Record created successfully'
                }

    @token_required
    def upload_xray(self):
        '''
            | @Route /records/upload_xray POST
            | @Access Private
            | @Desc : This function runs in parallel with `records.controllers.create()`. After the patient record is recorded
                into the SQLite3 database, the uploaded x-ray image and the patient's NRIC will be forwarded to the computing server 
                for inference. The diagnosis result and diagnosis confidence will be returned to the client.

            * Example input data for testing:
            
            .. code-block:: python

                import requests

                files = {'xray' : open('path/to/file.png', 'rb')}
                payload = {'nric' : 'G123456N'}

                requests.post('https://host/records/upload_xray', data=payload, files=files)

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

            # Dummy diagnosis result
            url = f'http://{COMPUTING_SERVER_IP}:{COMPUTING_SERVER_PORT}/predict_single_image'
            with open(os.path.join(IMG_UPLOAD_FOLDER, nric, filename), 'rb') as f:
                files = {'xray' : f}
                res = requests.post(url, files=files).json()
            
            result = res['_label']
            confidence = res['_confidence']

            # Store diagnosis result
            query = f'INSERT INTO DIAGNOSIS VALUES("{nric}", "{by_staff_id}", "{date_time}", "{result}", {confidence}, "{xray_img_url}");'
            results = execute_query(query, type="insert")

            if(results == "query_error"):
                return {
                    '_code' : 'failed',
                    'msg' : 'Something wrong happened'
                }
            else:
                return {
                    '_code' : 'success',
                    'msg' : 'Diagnosis recorded, file uploaded successfully ... ',
                    'payload' : {
                        'result' : result,
                        'confidence' : f'{confidence*100:.2f}%'
                    }
                }

