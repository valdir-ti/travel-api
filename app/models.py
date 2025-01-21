import uuid
from app import db

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
