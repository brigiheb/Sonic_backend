from app import db

class Product(db.Model):
    __tablename__ = "product"

    id_product = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    img_path = db.Column(db.String(500), nullable=True)

    # Relationship: One product has many product_items
    items = db.relationship("ProductItem", backref="product", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        try:
            return f"<Product {self.name}>"
        except Exception as e:
            return f"<Product Error: {str(e)}>"
