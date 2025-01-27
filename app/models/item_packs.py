from app import db

item_packs = db.Table(
    "item_packs",
    db.Column("id_items", db.Integer, db.ForeignKey("boutique_items.id_items", ondelete="CASCADE"), primary_key=True),
    db.Column("id_pack", db.Integer, db.ForeignKey("packs.id", ondelete="CASCADE"), primary_key=True)
)
