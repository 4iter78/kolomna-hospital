from app import create_app
from controllers.MainController import main_controller
from controllers.UserRolesController import user_roles_controller
from controllers.UsersController import users_controller
from controllers.AuthController import auth_controller
from controllers.PermissionsController import permissions_controller
from controllers.MaterialBalancesController import material_balances_controller
from controllers.MaterialIssuesController import material_issues_controller
from controllers.StockDeliveriesController import stock_deliveries_controller
from controllers.SuppliersController import suppliers_controller
from controllers.MaterialTypesController import material_types_controller
from controllers.MaterialUnitsController import material_units_controller
from controllers.DepartmentController import department_controller
from controllers.MedicalMaterialsController import medical_materials_controller
from json import JSONEncoder
from dotenv import load_dotenv
import os


load_dotenv()

APP_PORT = os.getenv("APP_PORT")


class ModelEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, '__json__'):
            return o.__json__()
        else:
            return super(ModelEncoder, self).default(o)


if __name__ == '__main__':
    app = create_app()
    app.register_blueprint(auth_controller)
    app.register_blueprint(main_controller)
    app.register_blueprint(user_roles_controller)
    app.register_blueprint(users_controller)
    app.register_blueprint(permissions_controller)
    app.register_blueprint(material_balances_controller)
    app.register_blueprint(material_issues_controller)
    app.register_blueprint(stock_deliveries_controller)
    app.register_blueprint(suppliers_controller)
    app.register_blueprint(material_types_controller)
    app.register_blueprint(material_units_controller)
    app.register_blueprint(department_controller)
    app.register_blueprint(medical_materials_controller)
    app.json_encoder = ModelEncoder
    # запуск сервера локально по умолчанию на порту 5000 по протоколу HTTPS
    # app.run(debug=True, ssl_context='adhoc')
    # запуск сервера локально на порту 8000 по протоколу HTTP
    # app.run(debug=True,port=8000)
    app.run(
        host='0.0.0.0',
        port=APP_PORT,
        debug=True
    )
