from flask import Blueprint, request, jsonify
from app.models.boutique_items import BoutiqueItem
from app.models.packs import Pack
from app.models.item_packs import item_packs
from app import db

boutique_item_bp = Blueprint("boutique_items", __name__)

# Create a new boutique item with packs
@boutique_item_bp.route("/post_item", methods=["POST"])
def create_item():
    try:
        data = request.json
        if "name" not in data or "price" not in data or "id_boutique" not in data:
            return jsonify({"error": "Name, price, and id_boutique are required"}), 400

        # Create the boutique item
        new_item = BoutiqueItem(
            name=data["name"], 
            price=data["price"], 
            description=data.get("description"), 
            quantity=data.get("quantity", 1),
            id_boutique=data["id_boutique"]
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
                # Associate the pack with the item
                new_item.packs.append(existing_pack)
                created_packs.append({"id": existing_pack.id, "name": existing_pack.name, "price": existing_pack.price})

        db.session.commit()

        return jsonify({
            "message": "Item created successfully",
            "item": {
                "id_items": new_item.id_items,
                "name": new_item.name,
                "price": new_item.price,
                "description": new_item.description,
                "quantity": new_item.quantity,
                "id_boutique": new_item.id_boutique,
                "packs": created_packs
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Get all items
@boutique_item_bp.route("/get_items", methods=["GET"])
def get_items():
    try:
        items = BoutiqueItem.query.all()
        item_list = [
            {
                "id_items": i.id_items,
                "name": i.name,
                "price": i.price,
                "description": i.description,
                "quantity": i.quantity,
                "id_boutique": i.id_boutique,
                "packs": [{"id": p.id, "name": p.name, "price": p.price} for p in i.packs]
            }
            for i in items
        ]
        return jsonify(item_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Update a boutique item by ID
@boutique_item_bp.route("/update_item/<int:id_items>", methods=["PUT"])
def update_item(id_items):
    try:
        item = BoutiqueItem.query.get(id_items)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        data = request.json
        item.name = data.get("name", item.name)
        item.price = data.get("price", item.price)
        item.description = data.get("description", item.description)
        item.quantity = data.get("quantity", item.quantity)
        item.id_boutique = data.get("id_boutique", item.id_boutique)

        db.session.commit()

        return jsonify({
            "message": "Item updated successfully",
            "item": {
                "id_items": item.id_items,
                "name": item.name,
                "price": item.price,
                "description": item.description,
                "quantity": item.quantity,
                "id_boutique": item.id_boutique
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Delete a boutique item by ID
@boutique_item_bp.route("/delete_item/<int:id_items>", methods=["DELETE"])
def delete_item(id_items):
    try:
        item = BoutiqueItem.query.get(id_items)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        db.session.delete(item)
        db.session.commit()

        return jsonify({"message": "Item deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
