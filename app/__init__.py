from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_cors import CORS
from app.config.config import Config

# Initialize database
db = SQLAlchemy()
mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    mysql.init_app(app)
    CORS(app)

    # Import and register routes
    from app.routes.products import product_bp
    from app.routes.boutiques import boutique_bp  # Import boutiques blueprint
    from app.routes.boutique_items import boutique_item_bp
    from app.routes.packs import pack_bp
    from app.routes.product_items import product_item_bp
    from app.routes.users import user_bp  # NEW
    from app.routes.applications import application_bp  # ✅ NEW
    from app.routes.special_price_users import special_price_bp  # ✅ NEW
    from app.routes.demande_solde import demande_solde_bp  # ✅ NEW



    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(boutique_bp, url_prefix="/boutiques")  # Register boutiques blueprint
    app.register_blueprint(boutique_item_bp, url_prefix="/boutique_items")
    app.register_blueprint(pack_bp, url_prefix="/packs")
    app.register_blueprint(product_item_bp, url_prefix="/product_items")
    app.register_blueprint(user_bp, url_prefix="/users")  # NEW
    app.register_blueprint(application_bp, url_prefix="/applications")  # ✅ NEW
    app.register_blueprint(special_price_bp, url_prefix="/special_prices")  # ✅ NEW
    app.register_blueprint(demande_solde_bp, url_prefix="/demande_solde")  # ✅ NEW


    return app


