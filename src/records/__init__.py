from flask import Blueprint

records_routes = Blueprint("records", __name__, url_prefix="/records")

from . import controllers 
from . import views

controller = controllers.RecordController()
view = views.RecordView()

# Register endpoints for all controller functions
records_routes.add_url_rule('/create_record', 'records_controllers_create_record', controller.create_record, methods=['POST'])
records_routes.add_url_rule('/get_record', 'records_controllers_get_record', controller.get_record, methods=['POST'])
records_routes.add_url_rule('/update_record', 'records_controllers_update_record', controller.update_record, methods=['POST'])
records_routes.add_url_rule('/delete_record', 'records_controllers_delete_record', controller.delete_record, methods=['POST'])

# Register endpoints for all view functions
records_routes.add_url_rule('/create', 'records_views_create', view.create_view, methods=['GET'])
records_routes.add_url_rule('/list', 'records_views_list', view.list_view, methods=['GET'])