from flask import Blueprint

records_routes = Blueprint("records", __name__, url_prefix="/records")

from . import controllers 
from . import views

# Register endpoints for all controller functions
controller = controllers.RecordsController()
records_routes.add_url_rule("/create", "records_controllers_create", controller.create, methods=['POST'])
records_routes.add_url_rule("/upload_xray", "records_controllers_upload_xray", controller.upload_xray, methods=['POST'])
records_routes.add_url_rule("/get_diagnosis", "records_controllers_get_diagnosis", controller.get_diagnosis, methods=['POST'])

# Register endpoints for all view functions
view = views.RecordsView()
records_routes.add_url_rule('/list', "records_views_list", view.list_view, methods=['GET'])
records_routes.add_url_rule('/search', "records_views_search", view.search_view, methods=['GET'])
records_routes.add_url_rule('/update', "records_views_update", view.update_view, methods=['GET'])
records_routes.add_url_rule('/create', "records_views_create", view.create_view, methods=['GET'])