from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app import db_connection

from decorators import access_control

from models.StockDeliveries import StockDeliveries
from models.DeliveryItems import DeliveryItems

from models.MedicalMaterials import MedicalMaterials
from models.Suppliers import Suppliers

db = db_connection


stock_deliveries_controller = Blueprint(
    'stock_deliveries_controller',
    __name__
)


# =====================================================
# DELIVERY LIST + CREATE
# =====================================================

@stock_deliveries_controller.route(
    '/delivery',
    methods=['GET', 'POST']
)
@access_control('delivery')
def handle_delivery():

    # =================================================
    # CREATE DELIVERY
    # =================================================

    if request.method == 'POST':

        data = request.form

        # =============================================
        # CREATE DELIVERY
        # =============================================

        new_delivery = StockDeliveries(
            supplier_id=data['supplier_id'],
            delivery_date=data['delivery_date'],
            document_number=data['document_number'],
            notes=data['notes']
        )

        db.session.add(new_delivery)

        db.session.commit()

        # =============================================
        # CREATE DELIVERY ITEMS
        # =============================================

        material_ids = request.form.getlist(
            'medical_material_id[]'
        )

        quantities = request.form.getlist(
            'quantity[]'
        )

        prices = request.form.getlist(
            'unit_price[]'
        )

        for i in range(len(material_ids)):

            item = DeliveryItems(
                stock_delivery_id=new_delivery.id,
                medical_material_id=material_ids[i],
                quantity=quantities[i],
                unit_price=prices[i]
            )

            db.session.add(item)

        db.session.commit()

        flash(
            f'Поставка #{new_delivery.id} успешно создана.',
            'success'
        )

        return redirect(
            url_for(
                'stock_deliveries_controller.handle_delivery'
            )
        )

    # =================================================
    # GET LIST
    # =================================================

    deliveries = StockDeliveries.query.all()

    result = []

    for delivery in deliveries:

        supplier = Suppliers.query.get(
            delivery.supplier_id
        )

        # =============================================
        # DELIVERY ITEMS
        # =============================================

        delivery_items = DeliveryItems.query.filter_by(
            stock_delivery_id=delivery.id
        ).all()

        items = []

        for item in delivery_items:

            material = MedicalMaterials.query.get(
                item.medical_material_id
            )

            txt_item = {
                "id": item.id,
                "medical_material_id":
                    item.medical_material_id,
                "medical_material":
                    material.name if material else '',
                "quantity":
                    item.quantity,
                "unit_price":
                    item.unit_price
            }

            items.append(txt_item)

        # =============================================
        # DELIVERY OBJECT
        # =============================================

        txt_delivery = {
            "id": delivery.id,
            "supplier_id":
                delivery.supplier_id,
            "supplier":
                supplier.name if supplier else '',
            "delivery_date":
                delivery.delivery_date,
            "document_number":
                delivery.document_number,
            "notes":
                delivery.notes,
            "delivery_items":
                items
        }

        result.append(txt_delivery)

    # =================================================
    # SUPPLIERS
    # =================================================

    suppliers = [

        {
            "id": supplier.id,
            "name": supplier.name
        }

        for supplier in Suppliers.query.all()
    ]

    # =================================================
    # MATERIALS
    # =================================================

    materials = [

        {
            "id": material.id,
            "name": material.name
        }

        for material in MedicalMaterials.query.all()
    ]

    return render_template(
        'delivery.html',
        title='Приём',
        deliveries=result,
        suppliers=suppliers,
        materials=materials,
        count=len(result)
    )


# =====================================================
# DELIVERY ITEM
# =====================================================

@stock_deliveries_controller.route(
    '/delivery/<delivery_id>',
    methods=['GET', 'PUT', 'DELETE']
)
@access_control('delivery')
def handle_delivery_item(delivery_id):

    delivery = StockDeliveries.query.get_or_404(
        delivery_id
    )

    # =================================================
    # GET ONE
    # =================================================

    if request.method == 'GET':

        supplier = Suppliers.query.get(
            delivery.supplier_id
        )

        delivery_items = DeliveryItems.query.filter_by(
            stock_delivery_id=delivery.id
        ).all()

        items = []

        for item in delivery_items:

            material = MedicalMaterials.query.get(
                item.medical_material_id
            )

            txt_item = {
                "id": item.id,
                "medical_material_id":
                    item.medical_material_id,
                "medical_material":
                    material.name if material else '',
                "quantity":
                    item.quantity,
                "unit_price":
                    item.unit_price
            }

            items.append(txt_item)

        response = {
            "id": delivery.id,
            "supplier_id":
                delivery.supplier_id,
            "supplier":
                supplier.name if supplier else '',
            "delivery_date":
                delivery.delivery_date,
            "document_number":
                delivery.document_number,
            "notes":
                delivery.notes,
            "delivery_items":
                items
        }

        return {

            "message": "success",

            "delivery": response
        }

    # =================================================
    # UPDATE
    # =================================================

    elif request.method == 'PUT':

        data = request.get_json()
        delivery.supplier_id = data[
            'supplier_id'
        ]
        delivery.delivery_date = data[
            'delivery_date'
        ]
        delivery.document_number = data[
            'document_number'
        ]
        delivery.notes = data[
            'notes'
        ]

        db.session.add(delivery)

        # =============================================
        # DELETE OLD ITEMS
        # =============================================

        old_items = DeliveryItems.query.filter_by(
            stock_delivery_id=delivery.id
        ).all()

        for item in old_items:
            db.session.delete(item)

        db.session.commit()

        # =============================================
        # ADD NEW ITEMS
        # =============================================

        for item_data in data['delivery_items']:

            new_item = DeliveryItems(
                stock_delivery_id=delivery.id,
                medical_material_id=item_data[
                    'medical_material_id'
                ],
                quantity=item_data[
                    'quantity'
                ],
                unit_price=item_data[
                    'unit_price'
                ]
            )

            db.session.add(new_item)

        db.session.commit()

        return {

            "message":
                f"Delivery {delivery.id} updated"
        }

    # =================================================
    # DELETE
    # =================================================

    elif request.method == 'DELETE':

        delivery_items = DeliveryItems.query.filter_by(
            stock_delivery_id=delivery.id
        ).all()

        for item in delivery_items:
            db.session.delete(item)

        db.session.delete(delivery)

        db.session.commit()

        return {
            "message":
                f"Delivery {delivery.id} successfully deleted"
        }
