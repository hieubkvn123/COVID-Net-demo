"""
    | Configurations storage for the application.

    * SECRET_KEY : The secret key used to verify JWT token.
    * TOKEN_TIMEOUT : Specifies the session limit time in minutes for JWT token.
    * DATABASE : Path to the SQLite3 database.
    * IMG_UPLOAD_FOLDER : The local path of the X-Ray images folder. 
    * ALLOWED_EXTENSIONS : The allowed image extensions.
    * COMPUTING_SERVER_IP : The IP address at which the model is hosted. You can deploy your own server and create
      an API endpoint "predict_single_image" and "predict_batch" as long as the response format is as followed:

    .. code-block:: python

        payload = {
            '_code' : 'success/failed',
            '_label' : 'positive/negative',
            '_confidence' : '[diagnosis confidence]'
        }


    * COMPUTING_SERVER_PORT : The port where the COVID-Net API listens to in the computing server.

"""

SECRET_KEY = b'FYP-COVID-DEMO-2022'
TOKEN_TIMEOUT = 60
DATABASE = 'db/fyp.db'
IMG_UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
COMPUTING_SERVER_IP = '128.199.205.5'
COMPUTING_SERVER_PORT = '8889'
DEFAULT_ROUTE_AUTHENTICATED = 'records.records_views_create'
DEFAULT_ROUTE_GUESS = 'authentication.auth_views_login'
