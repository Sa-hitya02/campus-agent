from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    """Initialize MongoDB connection."""
    mongo.init_app(app)
    print("✅ MongoDB connected successfully.")

def get_db():
    return mongo.db
