from flask import Blueprint, request, jsonify
from app.models.packs import Pack
from app import db

pack_bp = Blueprint("packs", __name__)

# Create a new pack
@pack_bp.route("/post_pack", methods=["POST"])
def create_pack():
    try:
        data = request.json
        if "name" not in data or "price" not in data:
            return jsonify({"error": "Pack name and price are required"}), 400

        new_pack = Pack(name=data["name"], price=data["price"])
        db.session.add(new_pack)
        db.session.commit()

        return jsonify({
            "message": "Pack created successfully",
            "pack": {
                "id": new_pack.id,
                "name": new_pack.name,
                "price": new_pack.price
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Get all packs
@pack_bp.route("/get_packs", methods=["GET"])
def get_packs():
    try:
        packs = Pack.query.all()
        pack_list = [{"id": p.id, "name": p.name, "price": p.price} for p in packs]
        return jsonify(pack_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Update a pack by ID
@pack_bp.route("/update_pack/<int:id>", methods=["PUT"])
def update_pack(id):
    try:
        pack = Pack.query.get(id)
        if not pack:
            return jsonify({"error": "Pack not found"}), 404

        data = request.json
        pack.name = data.get("name", pack.name)
        pack.price = data.get("price", pack.price)

        db.session.commit()

        return jsonify({
            "message": "Pack updated successfully",
            "pack": {
                "id": pack.id,
                "name": pack.name,
                "price": pack.price
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Delete a pack by ID
@pack_bp.route("/delete_pack/<int:id>", methods=["DELETE"])
def delete_pack(id):
    try:
        pack = Pack.query.get(id)
        if not pack:
            return jsonify({"error": "Pack not found"}), 404

        db.session.delete(pack)
        db.session.commit()

        return jsonify({"message": "Pack deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
