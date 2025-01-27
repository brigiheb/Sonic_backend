from app import db

class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    logo = db.Column(db.String(500), nullable=True)  # Path to logo image
    name = db.Column(db.String(255), nullable=False, unique=True)  # App name (unique)
    path = db.Column(db.String(500), nullable=False)  # Path to the app

    def __repr__(self):
        try:
            return f"<Application {self.name}>"
        except Exception as e:
            return f"<Application Error: {str(e)}>"
