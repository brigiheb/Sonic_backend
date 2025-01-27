from flask import Blueprint, request, jsonify
from app.models.application import Application
from app import db

application_bp = Blueprint("applications", __name__)

# Create a new application
@application_bp.route("/post_application", methods=["POST"])
def create_application():
    try:
        data = request.json
        if "name" not in data or "path" not in data:
            return jsonify({"error": "Name and Path are required"}), 400

        new_app = Application(
            logo=data.get("logo"),
            name=data["name"],
            path=data["path"]
        )

        db.session.add(new_app)
        db.session.commit()

        return jsonify({
            "message": "Application created successfully",
            "application": {
                "id": new_app.id,
                "logo": new_app.logo,
                "name": new_app.name,
                "path": new_app.path
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Get all applications
@application_bp.route("/get_applications", methods=["GET"])
def get_applications():
    try:
        applications = Application.query.all()
        app_list = [{
            "id": app.id,
            "logo": app.logo,
            "name": app.name,
            "path": app.path
        } for app in applications]

        return jsonify(app_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Get a single application by ID
@application_bp.route("/get_application/<int:id>", methods=["GET"])
def get_application(id):
    try:
        application = Application.query.get(id)
        if not application:
            return jsonify({"error": "Application not found"}), 404

        return jsonify({
            "id": application.id,
            "logo": application.logo,
            "name": application.name,
            "path": application.path
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Update an application by ID
@application_bp.route("/update_application/<int:id>", methods=["PUT"])
def update_application(id):
    try:
        application = Application.query.get(id)
        if not application:
            return jsonify({"error": "Application not found"}), 404

        data = request.json
        application.logo = data.get("logo", application.logo)
        application.name = data.get("name", application.name)
        application.path = data.get("path", application.path)

        db.session.commit()

        return jsonify({
            "message": "Application updated successfully",
            "application": {
                "id": application.id,
                "logo": application.logo,
                "name": application.name,
                "path": application.path
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Delete an application by ID
@application_bp.route("/delete_application/<int:id>", methods=["DELETE"])
def delete_application(id):
    try:
        application = Application.query.get(id)
        if not application:
            return jsonify({"error": "Application not found"}), 404

        db.session.delete(application)
        db.session.commit()

        return jsonify({"message": "Application deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
