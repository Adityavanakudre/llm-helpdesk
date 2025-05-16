from flask import Flask
from flask_cors import CORS
from auth import auth_bp  # ✅ Import from the flat structure
from tickets import tickets_bp

app = Flask(__name__)
CORS(app)

# ✅ Register both blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(tickets_bp)

@app.route("/health")
def health_check():
    return {"status": "running"}

if __name__ == "__main__":
    app.run(debug=True)
