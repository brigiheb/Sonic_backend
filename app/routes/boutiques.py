from flask import Blueprint, request, jsonify
from app.models.boutique import Boutique
from app import db

boutique_bp = Blueprint("boutiques", __name__)

# Create a new boutique
@boutique_bp.route("/post_boutique", methods=["POST"])
def create_boutique():
    try:
        data = request.json
        if "name" not in data:
            return jsonify({"error": "Boutique name is required"}), 400

        new_boutique = Boutique(name=data["name"], img_path=data.get("img_path"))
        db.session.add(new_boutique)
        db.session.commit()

        return jsonify({
            "message": "Boutique created successfully",
            "boutique": {
                "id_boutique": new_boutique.id_boutique,
                "name": new_boutique.name,
                "img_path": new_boutique.img_path
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Get all boutiques
@boutique_bp.route("/get_boutiques", methods=["GET"])
def get_boutiques():
    try:
        boutiques = Boutique.query.all()
        boutique_list = [
            {
                "id_boutique": b.id_boutique,
                "name": b.name,
                "img_path": b.img_path
            } for b in boutiques
        ]
        return jsonify(boutique_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Update a boutique by ID
@boutique_bp.route("/update_boutique/<int:id_boutique>", methods=["PUT"])
def update_boutique(id_boutique):
    try:
        boutique = Boutique.query.get(id_boutique)
        if not boutique:
            return jsonify({"error": "Boutique not found"}), 404

        data = request.json
        boutique.name = data.get("name", boutique.name)
        boutique.img_path = data.get("img_path", boutique.img_path)

        db.session.commit()

        return jsonify({
            "message": "Boutique updated successfully",
            "boutique": {
                "id_boutique": boutique.id_boutique,
                "name": boutique.name,
                "img_path": boutique.img_path
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Delete a boutique by ID
@boutique_bp.route("/delete_boutique/<int:id_boutique>", methods=["DELETE"])
def delete_boutique(id_boutique):
    try:
        boutique = Boutique.query.get(id_boutique)
        if not boutique:
            return jsonify({"error": "Boutique not found"}), 404

        db.session.delete(boutique)
        db.session.commit()

        return jsonify({"message": "Boutique deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
