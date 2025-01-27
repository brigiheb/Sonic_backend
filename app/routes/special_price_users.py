from flask import Blueprint, request, jsonify
from app.models.special_price_user import SpecialPriceUser
from app.models.user import User
from app.models.product_items import ProductItem
from app import db

special_price_bp = Blueprint("special_prices", __name__)

# ✅ Assign a special price to a user for a specific product item
@special_price_bp.route("/assign", methods=["POST"])
def assign_special_price():
    try:
        data = request.json
        if "user_id" not in data or "product_item_id" not in data or "special_price" not in data:
            return jsonify({"error": "user_id, product_item_id, and special_price are required"}), 400

        # Check if user and product item exist
        user = User.query.get(data["user_id"])
        product_item = ProductItem.query.get(data["product_item_id"])

        if not user:
            return jsonify({"error": "User not found"}), 404
        if not product_item:
            return jsonify({"error": "Product item not found"}), 404

        # Assign special price
        new_special_price = SpecialPriceUser(
            user_id=data["user_id"],
            product_item_id=data["product_item_id"],
            special_price=data["special_price"]
        )
        db.session.add(new_special_price)
        db.session.commit()

        return jsonify({"message": "Special price assigned successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Get all special prices
@special_price_bp.route("/get_all", methods=["GET"])
def get_all_special_prices():
    try:
        special_prices = SpecialPriceUser.query.all()
        result = [
            {
                "id": sp.id,
                "user_id": sp.user_id,
                "user_name": sp.user.nom,
                "product_item_id": sp.product_item_id,
                "product_item_name": sp.product_item.name,
                "special_price": sp.special_price
            }
            for sp in special_prices
        ]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Get special prices for a specific user
@special_price_bp.route("/get_user/<int:user_id>", methods=["GET"])
def get_special_prices_for_user(user_id):
    try:
        special_prices = SpecialPriceUser.query.filter_by(user_id=user_id).all()
        
        if not special_prices:
            return jsonify({"error": "No special prices found for this user"}), 404

        result = [
            {
                "id": sp.id,
                "product_item_id": sp.product_item_id,
                "product_item_name": sp.product_item.name,
                "special_price": sp.special_price
            }
            for sp in special_prices
        ]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Update a special price
@special_price_bp.route("/update/<int:id>", methods=["PUT"])
def update_special_price(id):
    try:
        special_price_entry = SpecialPriceUser.query.get(id)
        if not special_price_entry:
            return jsonify({"error": "Special price entry not found"}), 404

        data = request.json
        special_price_entry.special_price = data.get("special_price", special_price_entry.special_price)

        db.session.commit()

        return jsonify({"message": "Special price updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Delete a special price
@special_price_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_special_price(id):
    try:
        special_price_entry = SpecialPriceUser.query.get(id)
        if not special_price_entry:
            return jsonify({"error": "Special price entry not found"}), 404

        db.session.delete(special_price_entry)
        db.session.commit()

        return jsonify({"message": "Special price deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
