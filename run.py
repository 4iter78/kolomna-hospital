from app import create_app
from controllers.MainController import main_controller
from controllers.UserRolesController import user_roles_controller
from controllers.UsersController import users_controller
from controllers.CleanTimetableController import clean_timetable_controller
from controllers.DiagnosisesController import diagnosises_controller
from controllers.DrugsController import drugs_controller
from controllers.HealthCardsController import health_cards_controller
from controllers.PatientsController import patients_controller
from controllers.RoomsController import rooms_controller
from controllers.RoomTypeController import room_type_controller
from controllers.TreatmentTypesController import treatment_types_controller
from controllers.WorkTimetableController import work_timetable_controller
from controllers.AuthController import auth_controller
from controllers.PermissionsController import permissions_controller
from controllers.AppointmentsController import appointments_controller
from controllers.MaterialBalancesController import material_balances_controller
from controllers.MaterialIssuesController import material_issues_controller
from controllers.StockDeliveriesController import stock_deliveries_controller
from controllers.SuppliersController import suppliers_controller
from controllers.MaterialTypesController import material_types_controller
from controllers.MaterialUnitsController import material_units_controller
from controllers.DepartmentController import department_controller
from json import JSONEncoder


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
    app.register_blueprint(clean_timetable_controller)
    app.register_blueprint(diagnosises_controller)
    app.register_blueprint(drugs_controller)
    app.register_blueprint(health_cards_controller)
    app.register_blueprint(patients_controller)
    app.register_blueprint(rooms_controller)
    app.register_blueprint(room_type_controller)
    app.register_blueprint(treatment_types_controller)
    app.register_blueprint(work_timetable_controller)
    app.register_blueprint(permissions_controller)
    app.register_blueprint(appointments_controller)
    app.register_blueprint(material_balances_controller)
    app.register_blueprint(material_issues_controller)
    app.register_blueprint(stock_deliveries_controller)
    app.register_blueprint(suppliers_controller)
    app.register_blueprint(material_types_controller)
    app.register_blueprint(material_units_controller)
    app.register_blueprint(department_controller)
    app.json_encoder = ModelEncoder
    # запуск сервера локально по умолчанию на порту 5000 по протоколу HTTPS
    # app.run(debug=True, ssl_context='adhoc')
    # запуск сервера локально на порту 8000 по протоколу HTTP
    # app.run(debug=True,port=8000)
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
