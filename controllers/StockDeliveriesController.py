from datetime import datetime

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
from models.MaterialTypes import MaterialTypes
from models.MaterialUnits import MaterialUnits

from models.StockDeliveries import StockDeliveries
from models.DeliveryItems import DeliveryItems

from models.MedicalMaterials import MedicalMaterials
from models.Suppliers import Suppliers

db = db_connection


stock_deliveries_controller = Blueprint(
    'stock_deliveries_controller',
    __name__
)


@stock_deliveries_controller.route('/delivery',methods=['GET', 'POST'])
@access_control('delivery')
def handle_delivery():

    if request.method == 'POST':
        try:
            data = request.form
            new_delivery = StockDeliveries(
                supplier_id=data['supplier_id'],
                delivery_date=data['delivery_date'],
                document_number=data['document_number'],
                notes=data['notes']
            )
            db.session.add(new_delivery)
            db.session.commit()
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
            flash(f'Поставка #{new_delivery.id} успешно создана.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Поставка не может быть создана. {str(e)}", "danger")
        return redirect(url_for('stock_deliveries_controller.handle_delivery'))

    elif request.method == 'GET':
        deliveries = StockDeliveries.query.all()
        result = []
        for delivery in deliveries:
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
                material_type = None
                material_unit = None

                if material:
                    material_type = MaterialTypes.query.get(
                        material.material_type_id
                    )
                    material_unit = MaterialUnits.query.get(
                        material.material_unit_id
                    )
                txt_item = {
                    "id": item.id,
                    "medical_material_id":
                        item.medical_material_id,
                    "medical_material":
                        material.name if material else '',
                    "material_type_id":
                        material.material_type_id if material else '',
                    "material_type":
                        material_type.name if material else '',
                    "material_unit_id":
                        material.material_unit_id if material else '',
                    "material_unit":
                        material_unit.short_name if material else '',
                    "quantity":
                        f'{item.quantity} {material_unit.short_name}' if material else '',
                    "unit_price":
                        item.unit_price
                }
                items.append(txt_item)
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
        suppliers = [
            {
                "id": supplier.id,
                "name": supplier.name
            }
            for supplier in Suppliers.query.all()
        ]
        materials = [
            {
                "id": material.id,
                "name": material.name,
                "material_type_id": material.material_type_id,
                "material_unit_id": material.material_unit_id
            }
            for material in MedicalMaterials.query.all()
        ]
        material_types = [
            {
                "id": material_type.id,
                "name": material_type.name
            }
            for material_type in MaterialTypes.query.all()
        ]
        material_units = [
            {
                "id": material_unit.id,
                "name": material_unit.short_name
            }
            for material_unit in MaterialUnits.query.all()
        ]
        today = datetime.now().strftime("%Y-%m-%d")
        return render_template(
            'delivery.html',
            title='Поступление медицинских материалов на склад',
            deliveries=result,
            suppliers=suppliers,
            materials=materials,
            material_types=material_types,
            material_units=material_units,
            today=today,
            count=len(result)
        )


@stock_deliveries_controller.route('/delivery/<delivery_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control('delivery')
def handle_delivery_item(delivery_id):

    delivery = StockDeliveries.query.get_or_404(
        delivery_id
    )

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
            material_type = None
            material_unit = None
            if material:
                material_type = MaterialTypes.query.get(
                    material.material_type_id
                )
                material_unit = MaterialUnits.query.get(
                    material.material_unit_id
                )
            txt_item = {
                "id": item.id,
                "medical_material_id":
                    item.medical_material_id,
                "medical_material":
                    material.name if material else '',
                "material_type_id":
                    material.material_type_id if material else '',
                "material_type":
                    material_type.name if material else '',
                "material_unit_id":
                    material.material_unit_id if material else '',
                "material_unit":
                    material_unit.short_name if material else '',
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

    elif request.method == 'PUT':
        try:
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
            old_items = DeliveryItems.query.filter_by(
                stock_delivery_id=delivery.id
            ).all()

            for item in old_items:
                db.session.delete(item)
            for item_data in data['delivery_items']:
                db.session.add(
                    DeliveryItems(
                        stock_delivery_id=delivery.id,
                        medical_material_id=item_data['medical_material_id'],
                        quantity=item_data['quantity'],
                        unit_price=item_data['unit_price']
                    )
                )
            db.session.commit()
            return {"success": True, "message": f"Поступление {delivery.id} успешно обновлено"}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Поступление {delivery.id} не может быть обновлено. {str(e)}"}, 400

    elif request.method == 'DELETE':
        try:
            delivery_items = DeliveryItems.query.filter_by(
                stock_delivery_id=delivery.id
            ).all()
            for item in delivery_items:
                db.session.delete(item)
            db.session.delete(delivery)
            db.session.commit()
            return {"success": True, "message": f"Поступление {delivery.id} успешно удалена"}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Поступление {delivery.name} не может быть удалена. {str(e)}"}, 400

