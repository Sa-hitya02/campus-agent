from flask import Flask
from flask_cors import CORS
from config import Config
from utils.db import init_db
from routes.complaint_routes import complaint_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize DB
init_db(app)

# Register blueprints
app.register_blueprint(complaint_bp, url_prefix="/api/complaints")

@app.route("/")
def health():
    return {"status": "Smart Campus Complaint Agent is running 🧠"}, 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
