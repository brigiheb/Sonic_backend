from app import db
from app.models.product_item_packs import product_item_packs  # Import the association table

class ProductItem(db.Model):
    __tablename__ = "product_items"

    id_item = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Foreign Key linking to Product
    id_product = db.Column(db.Integer, db.ForeignKey("product.id_product", ondelete="CASCADE"), nullable=False)

    # Many-to-Many relationship: A product item can have multiple packs
    packs = db.relationship("Pack", secondary=product_item_packs, backref=db.backref("product_items", lazy="dynamic"))

    def __repr__(self):
        try:
            return f"<ProductItem {self.name} - {self.price}£>"
        except Exception as e:
            return f"<ProductItem Error: {str(e)}>"
