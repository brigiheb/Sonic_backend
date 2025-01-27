from flask import Blueprint, request, jsonify
from app.models.product import Product
from app.models.product_items import ProductItem
from app.models.packs import Pack
from app.models.product_item_packs import product_item_packs
from app import db

product_bp = Blueprint("products", __name__)

# ✅ Create a new product
@product_bp.route("/post_product", methods=["POST"])
def create_product():
    try:
        data = request.json
        if "name" not in data:
            return jsonify({"error": "Product name is required"}), 400

        new_product = Product(name=data["name"], img_path=data.get("img_path"))
        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "message": "Product created successfully",
            "product": {
                "id_product": new_product.id_product,
                "name": new_product.name,
                "img_path": new_product.img_path
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Get all products
@product_bp.route("/get_products", methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        product_list = [{"id_product": p.id_product, "name": p.name, "img_path": p.img_path} for p in products]
        return jsonify(product_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Update a product by ID
@product_bp.route("/update_product/<int:id_product>", methods=["PUT"])
def update_product(id_product):
    try:
        product = Product.query.get(id_product)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        data = request.json
        product.name = data.get("name", product.name)
        product.img_path = data.get("img_path", product.img_path)

        db.session.commit()

        return jsonify({
            "message": "Product updated successfully",
            "product": {
                "id_product": product.id_product,
                "name": product.name,
                "img_path": product.img_path
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Delete a product by ID
@product_bp.route("/delete_product/<int:id_product>", methods=["DELETE"])
def delete_product(id_product):
    try:
        product = Product.query.get(id_product)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": "Product deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Get all products with their items and associated packs
@product_bp.route("/get_products_with_packs", methods=["GET"])
def get_products_with_packs():
    try:
        products = Product.query.all()
        product_list = []

        for product in products:
            product_data = {
                "id_product": product.id_product,
                "name": product.name,
                "img_path": product.img_path,
                "items": []
            }

            for item in product.items:
                item_data = {
                    "id_item": item.id_item,
                    "name": item.name,
                    "price": item.price,
                    "description": item.description,
                    "quantity": item.quantity,
                    "packs": []
                }

                # Fetch associated packs for each product item
                for pack in item.packs:
                    pack_data = {
                        "id_pack": pack.id,
                        "name": pack.name,
                        "price": pack.price
                    }
                    item_data["packs"].append(pack_data)

                product_data["items"].append(item_data)

            product_list.append(product_data)

        return jsonify(product_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Get products with only pack name and pack price
@product_bp.route("/get_products_packs", methods=["GET"])
def get_products_packs():
    try:
        products = Product.query.all()
        product_list = []

        for product in products:
            packs_data = set()  # Use a set to avoid duplicate packs

            for item in product.items:
                for pack in item.packs:
                    packs_data.add((pack.name, pack.price))  # Store only name and price

            product_data = {
                "product_name": product.name,
                "packs": [{"pack_name": name, "pack_price": price} for name, price in packs_data]
            }

            product_list.append(product_data)

        return jsonify(product_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Update product's associated packs
@product_bp.route("/update_product_packs/<int:product_id>", methods=["PUT"])
def update_product_packs(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        data = request.json
        if "packs" not in data:
            return jsonify({"error": "Packs list is required"}), 400

        # Remove all existing pack associations for this product
        for item in product.items:
            item.packs.clear()

        # Add new packs from request data
        for pack_data in data["packs"]:
            pack = Pack.query.filter_by(name=pack_data["pack_name"], price=pack_data["pack_price"]).first()
            if not pack:
                pack = Pack(name=pack_data["pack_name"], price=pack_data["pack_price"])
                db.session.add(pack)
                db.session.flush()  # Generate the ID without committing

            # Associate new pack with each product item
            for item in product.items:
                item.packs.append(pack)

        db.session.commit()

        return jsonify({"message": "Product packs updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Delete all pack associations for a product
@product_bp.route("/delete_product_packs/<int:product_id>", methods=["DELETE"])
def delete_product_packs(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Remove all associated packs for this product
        for item in product.items:
            item.packs.clear()

        db.session.commit()

        return jsonify({"message": "All packs removed from the product successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
