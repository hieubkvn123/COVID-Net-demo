from flask import render_template, request
from utils.tokens import token_required, username_from_token

class RecordView:
    def __init__(self):
        super(RecordView, self).__init__()

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