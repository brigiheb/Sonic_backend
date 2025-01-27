from app import db

class Boutique(db.Model):
    __tablename__ = "boutique"

    id_boutique = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    img_path = db.Column(db.String(500), nullable=True)

    # Relationship: One boutique has many boutique_items
    items = db.relationship("BoutiqueItem", backref="boutique", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        try:
            return f"<Boutique {self.name}>"
        except Exception as e:
            return f"<Boutique Error: {str(e)}>"
