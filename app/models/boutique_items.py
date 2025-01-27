from app import db
from app.models.item_packs import item_packs  # Import the many-to-many table

class BoutiqueItem(db.Model):
    __tablename__ = "boutique_items"

    id_items = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Foreign Key linking to Boutique
    id_boutique = db.Column(db.Integer, db.ForeignKey("boutique.id_boutique", ondelete="CASCADE"), nullable=False)

    # Many-to-Many relationship: An item can have multiple packs
    packs = db.relationship("Pack", secondary=item_packs, backref=db.backref("items", lazy="dynamic"))

    def __repr__(self):
        try:
            return f"<BoutiqueItem {self.name} - {self.price}£>"
        except Exception as e:
            return f"<BoutiqueItem Error: {str(e)}>"
