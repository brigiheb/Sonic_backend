from app import db

product_item_packs = db.Table(
    "product_item_packs",
    db.Column("id_item", db.Integer, db.ForeignKey("product_items.id_item", ondelete="CASCADE"), primary_key=True),
    db.Column("id_pack", db.Integer, db.ForeignKey("packs.id", ondelete="CASCADE"), primary_key=True)
)
