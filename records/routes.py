import os
import datetime
import requests
from flask import Blueprint
from flask import request, render_template
from werkzeug.utils import secure_filename

from utils.db import execute_query
from utils.tokens import token_required, username_from_token
from config import IMG_UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from config import COMPUTING_SERVER_IP, COMPUTING_SERVER_PORT

records_routes = Blueprint("records", __name__, url_prefix="/records")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@records_routes.route("/create", methods=['POST'])
@token_required
def create():
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
        # [INFO] NEED TO TAKE INTO ACCOUNT IMG URL LATER.
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

@records_routes.route("/upload_xray", methods=['POST'])
@token_required
def upload_xray():
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
        if xray_image and allowed_file(xray_image.filename):
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

@records_routes.route('/list', methods=['GET'])
@token_required
def list_view():
    token = request.cookies.get('access_token')
    username = username_from_token(token)

    # Get all records and return
    query = "SELECT d.patient_nric_fin, pr.fname || ' ' || pr.lname AS name, d.date_time, d.result FROM DIAGNOSIS d JOIN PATIENT_RECORD pr ON d.patient_nric_fin=pr.nric_fin ORDER BY d.date_time;"
    results = execute_query(query)
    print(results)

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
