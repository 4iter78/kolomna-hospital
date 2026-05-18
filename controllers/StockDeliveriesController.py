from flask import redirect, url_for, flash, request, Blueprint, render_template

from app import db_connection

from models.StockDeliveries import StockDeliveries
from models.Suppliers import Suppliers

from decorators import access_control

db = db_connection

stock_deliveries_controller = Blueprint(
    'stock_deliveries_controller',
    __name__
)


@stock_deliveries_controller.route(
    '/delivery',
    methods=['POST', 'GET']
)
@access_control('delivery')
def handle_delivery():

    if request.method == 'POST':

        data = request.get_json() if request.is_json else request.form

        new_delivery = StockDeliveries(
            supplier_id=data['supplier_id'],
            delivery_date=data['delivery_date'],
            document_number=data['document_number'],
            notes=data['notes']
        )

        db.session.add(new_delivery)
        db.session.commit()

        flash(
            f'Поставка {new_delivery.id} успешно создана.',
            'success'
        )

        return redirect(
            url_for(
                'stock_deliveries_controller.handle_delivery'
            )
        )

    elif request.method == 'GET':

        deliveries = StockDeliveries.query.all()

        results = []

        for delivery in deliveries:

            supplier = Suppliers.query.get(
                delivery.supplier_id
            )

            txt_delivery = {
                "id": delivery.id,
                "supplier_id": delivery.supplier_id,
                "supplier": supplier.name if supplier else '',
                "delivery_date": delivery.delivery_date,
                "document_number": delivery.document_number,
                "notes": delivery.notes
            }

            results.append(txt_delivery)

        suppliers = [
            {
                "id": s.id,
                "name": s.name
            }
            for s in Suppliers.query.all()
        ]

        return render_template(
            'delivery.html',
            title='Приём',
            deliveries=results,
            suppliers=suppliers,
            count=len(results)
        )


@stock_deliveries_controller.route(
    '/delivery/<delivery_id>',
    methods=['GET', 'PUT', 'DELETE']
)
@access_control('delivery')
def handle_delivery_item(delivery_id):

    delivery = StockDeliveries.query.get_or_404(
        delivery_id
    )

    if request.method == 'GET':

        supplier = Suppliers.query.get(
            delivery.supplier_id
        )

        response = {
            "id": delivery.id,
            "supplier_id": delivery.supplier_id,
            "supplier": supplier.name if supplier else '',
            "delivery_date": delivery.delivery_date,
            "document_number": delivery.document_number,
            "notes": delivery.notes
        }

        return {
            "message": "success",
            "delivery": response
        }

    elif request.method == 'PUT':

        data = request.get_json()

        delivery.supplier_id = data['supplier_id']
        delivery.delivery_date = data['delivery_date']
        delivery.document_number = data['document_number']
        delivery.notes = data['notes']

        db.session.add(delivery)

        db.session.commit()

        return {
            "message":
                f"Delivery {delivery.id} successfully updated"
        }

    elif request.method == 'DELETE':

        db.session.delete(delivery)

        db.session.commit()

        return {
            "message":
                f"Delivery {delivery.id} successfully deleted"
        }
