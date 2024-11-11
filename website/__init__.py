from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from .models import db, User
from .chat import chat, socketio   # Import chat blueprint and socketio
from config import Config

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    app.config.from_object(Config)

    # Initialize SQLAlchemy
    db.init_app(app)
    csrf.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register the existing blueprints (authentication, user, etc.)
    from .auth import auth
    from .user import user
    from .utils import utils
    from .manager import manager
    from .admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(utils)
    app.register_blueprint(manager)
    app.register_blueprint(admin)
    app.register_blueprint(chat)  # Register the chat blueprint

    # Initialize SocketIO with the Flask app
    socketio.init_app(app, cors_allowed_origins="*")

    # Create Admin User
    def createAdminUser():
        try:
            with app.app_context():
                searchForAdmin = User.query.filter_by(auth='admin').first()
                if not searchForAdmin:
                    print("No admin user, attempting to create an admin user...")
                    createAdmin = User(
                        username='admin',
                        email='admin@admin.com',
                        auth='admin'
                    )
                    createAdmin.set_password('password')
                    db.session.add(createAdmin)
                    db.session.commit()
                    print("Admin user has been created successfully")
        except Exception as e:
            print(f"Error creating admin user: {e}")

    with app.app_context():
        db.create_all()  # Create database tables
        createAdminUser()  # Create admin user if none exists

    return app
