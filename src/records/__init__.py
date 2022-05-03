from flask import Blueprint

records_routes = Blueprint("records", __name__, url_prefix="/records")

from . import controllers 
from . import views

controller = controllers.RecordController()
view = views.RecordView()

# Register endpoints for all controller functions
records_routes.add_url_rule('/create_record', 'records_controllers_create', controller.create, methods=['POST'])

# Register endpoints for all view functions
records_routes.add_url_rule('/create', 'records_views_create', view.create_view, methods=['GET'])