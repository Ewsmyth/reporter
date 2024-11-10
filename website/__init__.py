from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from .models import db, User
from .chat import chat, socketio   # Import chat blueprint and socketio

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')


    app.config['SECRET_KEY'] = "aabbccddeeffgg"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reporter-data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

    def create_specific_users():
        """Creates three specific users: ewsmyth, apwindu, and cbrober."""
        try:
            with app.app_context():  # Ensure the app context is active
                # Define the three users
                users_to_create = [
                    {
                        'username': 'ewsmyth',
                        'email': 'ewsmyth@example.com',
                        'password': 'password',
                        'auth': 'user',
                        'firstname': 'Emmett',
                        'lastname': 'Smyth'
                    },
                    {
                        'username': 'apwindu',
                        'email': 'apwindu@example.com',
                        'password': 'password',
                        'auth': 'user',
                        'firstname': 'Alex',
                        'lastname': 'Windus'
                    },
                    {
                        'username': 'cbrober',
                        'email': 'cbrober@example.com',
                        'password': 'password',
                        'auth': 'user',
                        'firstname': 'Cameron',
                        'lastname': 'Roberts'
                    }
                ]
                
                # Iterate over the users and create them if they don't exist
                for user_data in users_to_create:
                    # Check if the user already exists by email
                    existing_user = User.query.filter_by(email=user_data['email']).first()
                    
                    if not existing_user:
                        print(f"Creating user: {user_data['username']}")
                        
                        # Create a new User object
                        new_user = User(
                            username=user_data['username'],
                            email=user_data['email'],
                            auth=user_data['auth'],
                            firstname=user_data['firstname'],
                            lastname=user_data['lastname']
                        )
                        
                        # Set the user's password
                        new_user.set_password(user_data['password'])
                        
                        # Add the new user to the session
                        db.session.add(new_user)
                    else:
                        print(f"User {user_data['username']} already exists.")
                
                # Commit the changes to the database
                db.session.commit()
                print("All specified users have been created successfully")
        
        except Exception as e:
            print(f"Error creating users: {e}")


    with app.app_context():
        db.create_all()  # Create database tables
        createAdminUser()  # Create admin user if none exists
        create_specific_users() # Call the function to create the users

    return app
