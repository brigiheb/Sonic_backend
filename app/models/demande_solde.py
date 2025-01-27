from app import db
from sqlalchemy.dialects.mysql import ENUM
from datetime import datetime

class DemandeSolde(db.Model):
    __tablename__ = "demande_solde"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    nom = db.Column(db.String(255), nullable=False)  # Store the user's name for quick reference
    montant = db.Column(db.Float, nullable=False)  # Requested amount
    date_demande = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Request date

    # ✅ Etat column as ENUM with 3 possible values
    etat = db.Column(ENUM("En attente", "Approuvé", "Rejeté", name="etat_enum"), nullable=False, default="En attente")

    # Relationships
    user = db.relationship("User", backref="demandes_solde")

    def __repr__(self):
        try:
            return f"<DemandeSolde User: {self.nom}, Montant: {self.montant}, Etat: {self.etat}>"
        except Exception as e:
            return f"<DemandeSolde Error: {str(e)}>"
