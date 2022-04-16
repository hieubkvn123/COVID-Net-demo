from flask import Blueprint

auth_routes = Blueprint("authentication", __name__, url_prefix="/auth")

from . import controllers 
from . import views

controller = controllers.AuthController()

# Register endpoints for all controller functions
auth_routes.add_url_rule('/login', "auth_controllers_login", controller.login, methods=['POST'])
auth_routes.add_url_rule('/logout', "auth_controllers_logout", controller.logout, methods=['GET'])
