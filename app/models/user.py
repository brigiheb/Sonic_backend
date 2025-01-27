from app import db
from sqlalchemy.dialects.mysql import ENUM  # ✅ Import ENUM type

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo = db.Column(db.String(500), nullable=True)
    nom = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telephone = db.Column(db.String(20), unique=True, nullable=False)
    solde = db.Column(db.Float, nullable=False, default=0.0)
    
    # ✅ Use ENUM type for etat
    etat = db.Column(ENUM("Active", "Not Active", name="user_status"), nullable=False, default="Active")

    def __repr__(self):
        try:
            return f"<User {self.nom} - {self.email} - {self.etat}>"
        except Exception as e:
            return f"<User Error: {str(e)}>"
