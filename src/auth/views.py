from flask import render_template

class AuthView:
    def __init__(self):
        super(AuthView, self).__init__()

    def login_view(self):
        '''
            | @Route / GET
            | @Access Public/Private
            | @Desc : First page to be seen by the users. The API will check if a JWT token exists
            in the session. If the token exists, user will be redirected to the create records page. Else, 
            the login page will be rendered. 
            |
	    '''
        return render_template('login.html')
