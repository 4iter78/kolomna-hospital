from PP_2025.app import create_app
from PP_2025.controllers.MainController import main_controller
from PP_2025.controllers.UserRolesController import user_roles_controller
from PP_2025.controllers.UsersController import users_controller
from json import JSONEncoder


class ModelEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, '__json__'):
            return o.__json__()
        else:
            return super(ModelEncoder, self).default(o)


if __name__ == '__main__':
    app = create_app()
    app.register_blueprint(main_controller)
    app.register_blueprint(user_roles_controller)
    app.register_blueprint(users_controller)
    app.json_encoder = ModelEncoder
    # запуск сервера локально по умолчанию на порту 5000 по протоколу HTTPS
    # app.run(debug=True, ssl_context='adhoc')
    # запуск сервера локально на порту 8000 по протоколу HTTP
    app.run(debug=True,port=8000)
