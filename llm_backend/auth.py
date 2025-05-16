# auth.py
from flask import Blueprint, request, jsonify
from db import db
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    if role not in ["user", "it"]:
        return jsonify({"error": "Role must be 'user' or 'it'"}), 400

    if db.users.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 409

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    db.users.insert_one({
        "name": name,
        "email": email,
        "password": hashed_pw,
        "role": role
    })

    return jsonify({"message": "Registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return jsonify({"error": "Invalid password"}), 401

    return jsonify({
        "message": "Login successful",
        "user_id": str(user["_id"]),
        "role": user["role"],
        "name": user["name"]
    }), 200
