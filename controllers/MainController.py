from flask import Blueprint, render_template

main_controller = Blueprint('main_controller', __name__)


# маршрут главная страница
@main_controller.route('/')
def hello():
    return render_template('main_page.html', title='Приложение ЦРБ')
        #{"hello": "world"}
