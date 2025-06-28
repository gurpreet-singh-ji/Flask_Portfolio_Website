from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create extensions (without importing models yet!)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Where unauthenticated users will be redirected

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    # 🔁 IMPORT User AFTER extensions are initialized to avoid circular import
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from app.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
