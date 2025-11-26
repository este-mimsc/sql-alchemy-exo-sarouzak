"""Minimal Flask application setup for the SQLAlchemy assignment."""
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import Config

# These extension instances are shared across the app and models
# so that SQLAlchemy can bind to the application context when the
# factory runs.
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    """Application factory used by Flask and the tests.

    The optional ``test_config`` dictionary can override settings such as
    the database URL to keep student tests isolated.
    """

    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here so SQLAlchemy is aware of them before migrations
    # or ``create_all`` run. Students will flesh these out in ``models.py``.
    import models  # noqa: F401

    @app.route("/")
    def index():
        """Simple sanity check route."""

        return jsonify({"message": "Welcome to the Flask + SQLAlchemy assignment"})

    @app.route("/users", methods=["GET", "POST"])
    def users():
        """List or create users."""
        
        if request.method == "GET":
            # Query all users and return as JSON list
            all_users = models.User.query.all()
            users_list = [
                {"id": user.id, "username": user.username}
                for user in all_users
            ]
            return jsonify(users_list), 200
        
        elif request.method == "POST":
            # Create a new user from JSON data
            data = request.get_json()
            username = data.get("username")
            
            if not username:
                return jsonify({"error": "username is required"}), 400
            
            # Create and save new user
            new_user = models.User(username=username)
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({"id": new_user.id, "username": new_user.username}), 201

    @app.route("/posts", methods=["GET", "POST"])
    def posts():
        """List or create posts."""
        
        if request.method == "GET":
            # Query all posts and include user information
            all_posts = models.Post.query.all()
            posts_list = [
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "user_id": post.user_id,
                    "username": post.user.username
                }
                for post in all_posts
            ]
            return jsonify(posts_list), 200
        
        elif request.method == "POST":
            # Create a new post tied to a valid user
            data = request.get_json()
            title = data.get("title")
            content = data.get("content")
            user_id = data.get("user_id")
            
            if not all([title, content, user_id]):
                return jsonify({"error": "title, content, and user_id are required"}), 400
            
            # Check if user exists
            user = db.session.get(models.User, user_id)

            if not user:
                return jsonify({"error": "User not found"}), 400
            
            # Create and save new post
            new_post = models.Post(title=title, content=content, user_id=user_id)
            db.session.add(new_post)
            db.session.commit()
            
            return jsonify({
                "id": new_post.id,
                "title": new_post.title,
                "content": new_post.content,
                "user_id": new_post.user_id
            }), 201

    return app


# Expose a module-level application for convenience with certain tools
app = create_app()


if __name__ == "__main__":
    # Running ``python app.py`` starts the development server.
    app.run(debug=True)