from flask import redirect, url_for, flash, request, Blueprint, render_template

from app import db_connection

from models.MaterialIssues import MaterialIssues
from models.Users import Users
from models.Departments import Departments

from decorators import access_control

db = db_connection

material_issues_controller = Blueprint(
    'material_issues_controller',
    __name__
)


@material_issues_controller.route(
    '/issue',
    methods=['POST', 'GET']
)
@access_control('issue')
def handle_issue():

    if request.method == 'POST':

        data = request.get_json() if request.is_json else request.form

        new_issue = MaterialIssues(
            from_user_id=data['from_user_id'],
            to_user_id=data['to_user_id'],
            issue_date=data['issue_date'],
            department_id=data['department_id'],
            notes=data['notes']
        )

        db.session.add(new_issue)

        db.session.commit()

        flash(
            f'Выдача {new_issue.id} успешно создана.',
            'success'
        )

        return redirect(
            url_for(
                'material_issues_controller.handle_issue'
            )
        )

    elif request.method == 'GET':

        issues = MaterialIssues.query.all()

        results = []

        for issue in issues:

            from_user = Users.query.get(
                issue.from_user_id
            )

            to_user = Users.query.get(
                issue.to_user_id
            )

            department = Departments.query.get(
                issue.department_id
            )

            txt_issue = {
                "id": issue.id,

                "from_user_id": issue.from_user_id,

                "from_user":
                    f'{from_user.surname} '
                    f'{from_user.name}'
                    if from_user else '',

                "to_user_id": issue.to_user_id,

                "to_user":
                    f'{to_user.surname} '
                    f'{to_user.name}'
                    if to_user else '',

                "issue_date": issue.issue_date,

                "department_id": issue.department_id,

                "department":
                    department.name
                    if department else '',

                "notes": issue.notes
            }

            results.append(txt_issue)

        users = [
            {
                "id": u.id,
                "name":
                    f'{u.surname} '
                    f'{u.name}'
            }
            for u in Users.query.all()
        ]

        departments = [
            {
                "id": d.id,
                "name": d.name
            }
            for d in Departments.query.all()
        ]

        return render_template(
            'issue.html',
            title='Выдача',
            issues=results,
            users=users,
            departments=departments,
            count=len(results)
        )


@material_issues_controller.route(
    '/issue/<issue_id>',
    methods=['GET', 'PUT', 'DELETE']
)
@access_control('issue')
def handle_issue_item(issue_id):

    issue = MaterialIssues.query.get_or_404(issue_id)

    if request.method == 'GET':

        response = {
            "id": issue.id,
            "from_user_id": issue.from_user_id,
            "to_user_id": issue.to_user_id,
            "issue_date": issue.issue_date,
            "department_id": issue.department_id,
            "notes": issue.notes
        }

        return {
            "message": "success",
            "issue": response
        }

    elif request.method == 'PUT':

        data = request.get_json()

        issue.from_user_id = data['from_user_id']
        issue.to_user_id = data['to_user_id']
        issue.issue_date = data['issue_date']
        issue.department_id = data['department_id']
        issue.notes = data['notes']

        db.session.add(issue)

        db.session.commit()

        return {
            "message":
                f"Issue {issue.id} successfully updated"
        }

    elif request.method == 'DELETE':

        db.session.delete(issue)

        db.session.commit()

        return {
            "message":
                f"Issue {issue.id} successfully deleted"
        }
    