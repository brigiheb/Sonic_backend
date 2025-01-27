from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db

user_bp = Blueprint("users", __name__)

# ✅ Create a new user
@user_bp.route("/post_user", methods=["POST"])
def create_user():
    try:
        data = request.json
        if "nom" not in data or "email" not in data or "telephone" not in data:
            return jsonify({"error": "Nom, Email, and Téléphone are required"}), 400

        # Validate etat
        etat_value = data.get("etat", "Active")
        if etat_value not in ["Active", "Not Active"]:
            return jsonify({"error": "Etat must be 'Active' or 'Not Active'"}), 400

        new_user = User(
            photo=data.get("photo"),
            nom=data["nom"],
            email=data["email"],
            telephone=data["telephone"],
            solde=data.get("solde", 0.0),
            etat=etat_value
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User created successfully",
            "user": {
                "id": new_user.id,
                "photo": new_user.photo,
                "nom": new_user.nom,
                "email": new_user.email,
                "telephone": new_user.telephone,
                "solde": new_user.solde,
                "etat": new_user.etat
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Get all users
@user_bp.route("/get_users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        user_list = [{
            "id": u.id,
            "photo": u.photo,
            "nom": u.nom,
            "email": u.email,
            "telephone": u.telephone,
            "solde": u.solde,
            "etat": u.etat
        } for u in users]
        return jsonify(user_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Get a single user by ID
@user_bp.route("/get_user/<int:id>", methods=["GET"])
def get_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "photo": user.photo,
            "nom": user.nom,
            "email": user.email,
            "telephone": user.telephone,
            "solde": user.solde,
            "etat": user.etat
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Update a user by ID
@user_bp.route("/update_user/<int:id>", methods=["PUT"])
def update_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.json

        # Validate etat
        etat_value = data.get("etat", user.etat)
        if etat_value not in ["Active", "Not Active"]:
            return jsonify({"error": "Etat must be 'Active' or 'Not Active'"}), 400

        user.photo = data.get("photo", user.photo)
        user.nom = data.get("nom", user.nom)
        user.email = data.get("email", user.email)
        user.telephone = data.get("telephone", user.telephone)
        user.solde = data.get("solde", user.solde)
        user.etat = etat_value

        db.session.commit()

        return jsonify({
            "message": "User updated successfully",
            "user": {
                "id": user.id,
                "photo": user.photo,
                "nom": user.nom,
                "email": user.email,
                "telephone": user.telephone,
                "solde": user.solde,
                "etat": user.etat
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Delete a user by ID
@user_bp.route("/delete_user/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
