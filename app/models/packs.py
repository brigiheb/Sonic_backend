from app import db

class Pack(db.Model):
    __tablename__ = "packs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        try:
            return f"<Pack {self.name} - {self.price}£>"
        except Exception as e:
            return f"<Pack Error: {str(e)}>"
