import os
import uuid
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Class Destination
class Destination(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    destination = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "country": self.country,
            "rating": self.rating,
        }
        
    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

with app.app_context():
    db.drop_all()
    db.create_all()

#default route
@app.route("/")
def home():
    return jsonify({ "message": "Welcome to travel API" })

# get destinations
@app.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination.to_dict() for destination in destinations])

# get specific destination
@app.route("/destinations/<destination_id>", methods=["GET"])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify(destination.to_dict())

    return ({ "error": "Destination not found" }), 404

# add destination
@app.route("/destinations", methods=["POST"])
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
@app.route("/destinations/<destination_id>", methods=["PUT"])
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
@app.route("/destinations/<destination_id>", methods=["DELETE"])
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        db.session.delete(destination)
        db.session.commit()
        return jsonify({ "message": "Destination deleted" })

    return jsonify({ "error": "Desination not found" }), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port)