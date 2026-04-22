from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt, jwt

from resources.auth import auth_bp
from resources.notes import notes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)