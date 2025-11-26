"""Database models for the Flask + SQLAlchemy assignment."""
from app import db


class User(db.Model):
    """User model - represents a blog user/author."""
    
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Username must be unique and required
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # Relationship: one user has many posts
    # backref='user' creates a 'user' attribute on Post objects
    # lazy=True means posts are loaded only when accessed
    posts = db.relationship('Post', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    """Post model - represents a blog post."""
    
    __tablename__ = 'posts'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Post content
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Foreign key to users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # The 'user' attribute is automatically created by the backref in User.posts
    
    def __repr__(self):
        return f'<Post {self.title}>'