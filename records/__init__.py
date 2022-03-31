from flask import Blueprint

records_routes = Blueprint("records", __name__, url_prefix="/records")

from . import controllers 
from . import views