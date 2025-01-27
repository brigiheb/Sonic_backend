from flask import Blueprint, request, jsonify
from app.models.product_items import ProductItem
from app.models.packs import Pack
from app.models.product_item_packs import product_item_packs
from app import db

product_item_bp = Blueprint("product_items", __name__)

# Create a new product item with packs
@product_item_bp.route("/post_item", methods=["POST"])
def create_item():
    try:
        data = request.json
        if "name" not in data or "price" not in data or "id_product" not in data:
            return jsonify({"error": "Name, price, and id_product are required"}), 400

        # Create the product item
        new_item = ProductItem(
            name=data["name"], 
            price=data["price"], 
            description=data.get("description"), 
            quantity=data.get("quantity", 1),
            id_product=data["id_product"]
        )
        db.session.add(new_item)
        db.session.flush()  # Flush to generate the item's ID without committing yet

        # Check if packs are provided in the request
        packs = data.get("packs", [])  # Packs should be a list of dictionaries: [{"name": ..., "price": ...}, ...]
        created_packs = []
        for pack_data in packs:
            if "name" in pack_data and "price" in pack_data:
                # Create or fetch the pack
                existing_pack = Pack.query.filter_by(name=pack_data["name"], price=pack_data["price"]).first()
                if not existing_pack:
                    existing_pack = Pack(name=pack_data["name"], price=pack_data["price"])
                    db.session.add(existing_pack)
                    db.session.flush()  # Flush to generate the pack's ID without committing yet
                # Associate the pack with the product item
                new_item.packs.append(existing_pack)
                created_packs.append({"id": existing_pack.id, "name": existing_pack.name, "price": existing_pack.price})

        db.session.commit()

        return jsonify({
            "message": "Product item created successfully",
            "item": {
                "id_item": new_item.id_item,
                "name": new_item.name,
                "price": new_item.price,
                "description": new_item.description,
                "quantity": new_item.quantity,
                "id_product": new_item.id_product,
                "packs": created_packs
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Get all product items
@product_item_bp.route("/get_items", methods=["GET"])
def get_items():
    try:
        items = ProductItem.query.all()
        item_list = [
            {
                "id_item": i.id_item,
                "name": i.name,
                "price": i.price,
                "description": i.description,
                "quantity": i.quantity,
                "id_product": i.id_product,
                "packs": [{"id": p.id, "name": p.name, "price": p.price} for p in i.packs]
            }
            for i in items
        ]
        return jsonify(item_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
