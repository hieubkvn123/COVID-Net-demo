from flask import Blueprint

diagnosis_routes = Blueprint("diagnosis", __name__, url_prefix="/diagnosis")

from . import controllers 
from . import views

# Register endpoints for all controller functions
controller = controllers.DiagnosisController()
diagnosis_routes.add_url_rule("/create_diagnosis", "records_controllers_create_diagnosis", controller.create_diagnosis, methods=['POST']) # Create diagnosis
diagnosis_routes.add_url_rule("/get_diagnosis", "records_controllers_get_diagnosis", controller.get_diagnosis, methods=['POST']) # View one diagnosis
diagnosis_routes.add_url_rule("/update_diagnosis", "records_controllers_update_diagnosis", controller.update_diagnosis, methods=['POST']) # Update diagnosis
diagnosis_routes.add_url_rule("/delete_diagnosis", "records_controllers_delete_diagnosis", controller.delete_diagnosis, methods=['POST']) # Delete diagnosis

# Register endpoints for all view functions
view = views.DiagnosisView()
diagnosis_routes.add_url_rule('/list', "records_views_list", view.list_view, methods=['GET']) # View all diagnosis records
diagnosis_routes.add_url_rule('/search', "records_views_search", view.search_view, methods=['GET']) 
# diagnosis_routes.add_url_rule('/update', "records_views_update", view.update_view, methods=['GET'])
# diagnosis_routes.add_url_rule('/create', "records_views_create", view.create_view, methods=['GET'])