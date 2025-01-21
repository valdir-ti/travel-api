from flask import Blueprint, jsonify, request
from app.models import Destination
from app import db

destinations_bp = Blueprint("destinations", __name__, url_prefix="/")

# get destinations
@destinations_bp.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination.to_dict() for destination in destinations])

# get specific destination
@destinations_bp.route("/destinations/<destination_id>", methods=["GET"])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify(destination.to_dict())

    return ({ "error": "Destination not found" }), 404

# add destination
@destinations_bp.route("/destinations", methods=["POST"])
def add_destination():
    data = request.get_json()
    new_destination = Destination(
        destination=data["destination"],
        country=data["country"],
        rating=data["rating"]
    )
    db.session.add(new_destination)
    db.session.commit()
    return jsonify(new_destination.to_dict())

# update desination
@destinations_bp.route("/destinations/<destination_id>", methods=["PUT"])
def update_destination(destination_id):
    data = request.get_json()
    destination = Destination.query.get(destination_id)
    if destination:
        destination.destination = data.get("destination", destination.destination)
        destination.country = data.get("country", destination.country)
        destination.rating = data.get("rating", destination.rating)

        db.session.commit()
        return jsonify(destination.to_dict())

    return jsonify({ "error": "Desination not found" }), 404

# Delete a destination
@destinations_bp.route("/destinations/<destination_id>", methods=["DELETE"])
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        db.session.delete(destination)
        db.session.commit()
        return jsonify({ "message": "Destination deleted" })

    return jsonify({ "error": "Desination not found" }), 404