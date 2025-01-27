from app import db

class SpecialPriceUser(db.Model):
    __tablename__ = "special_price_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_item_id = db.Column(db.Integer, db.ForeignKey("product_items.id_item", ondelete="CASCADE"), nullable=False)
    
    special_price = db.Column(db.Float, nullable=False)  # Custom price for the user

    # Relationships
    user = db.relationship("User", backref="special_prices")
    product_item = db.relationship("ProductItem", backref="special_prices")

    def __repr__(self):
        try:
            return f"<SpecialPriceUser User: {self.user_id}, ProductItem: {self.product_item_id}, Price: {self.special_price}>"
        except Exception as e:
            return f"<SpecialPriceUser Error: {str(e)}>"
