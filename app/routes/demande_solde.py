from flask import Blueprint, request, jsonify
from app.models.demande_solde import DemandeSolde
from app.models.user import User
from app import db

demande_solde_bp = Blueprint("demande_solde", __name__)

# ✅ Submit a balance request
@demande_solde_bp.route("/submit", methods=["POST"])
def submit_demande():
    try:
        data = request.json
        if "user_id" not in data or "montant" not in data:
            return jsonify({"error": "user_id and montant are required"}), 400

        # Check if user exists
        user = User.query.get(data["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Create the request
        new_demande = DemandeSolde(
            user_id=data["user_id"],
            nom=user.nom,  # Store user's name
            montant=data["montant"]
        )
        db.session.add(new_demande)
        db.session.commit()

        return jsonify({"message": "Balance request submitted successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Get all balance requests
@demande_solde_bp.route("/get_all", methods=["GET"])
def get_all_demandes():
    try:
        demandes = DemandeSolde.query.all()
        result = [
            {
                "id": d.id,
                "user_id": d.user_id,
                "nom": d.nom,
                "montant": d.montant,
                "date_demande": d.date_demande.strftime("%Y-%m-%d %H:%M:%S"),
                "etat": d.etat
            }
            for d in demandes
        ]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Get balance requests for a specific user
@demande_solde_bp.route("/get_user/<int:user_id>", methods=["GET"])
def get_user_demandes(user_id):
    try:
        demandes = DemandeSolde.query.filter_by(user_id=user_id).all()

        if not demandes:
            return jsonify({"error": "No balance requests found for this user"}), 404

        result = [
            {
                "id": d.id,
                "montant": d.montant,
                "date_demande": d.date_demande.strftime("%Y-%m-%d %H:%M:%S"),
                "etat": d.etat
            }
            for d in demandes
        ]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Update the request status
@demande_solde_bp.route("/update/<int:id>", methods=["PUT"])
def update_demande_status(id):
    try:
        demande = DemandeSolde.query.get(id)
        if not demande:
            return jsonify({"error": "Balance request not found"}), 404

        data = request.json
        if "etat" not in data or data["etat"] not in ["En attente", "Approuvé", "Rejeté"]:
            return jsonify({"error": "Etat must be 'En attente', 'Approuvé', or 'Rejeté'"}), 400

        demande.etat = data["etat"]
        db.session.commit()

        return jsonify({"message": "Balance request status updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ✅ Delete a balance request
@demande_solde_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_demande(id):
    try:
        demande = DemandeSolde.query.get(id)
        if not demande:
            return jsonify({"error": "Balance request not found"}), 404

        db.session.delete(demande)
        db.session.commit()

        return jsonify({"message": "Balance request deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
