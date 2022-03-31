from flask import Blueprint

auth_routes = Blueprint("authentication", __name__, url_prefix="/auth")

from . import controllers 
from . import views