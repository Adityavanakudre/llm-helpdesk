from flask import Blueprint, request, jsonify
from llm_service import classify_and_draft
from db import db
import datetime
from bson import ObjectId
from email_service import send_ticket_confirmation


tickets_bp = Blueprint("tickets", __name__)

@tickets_bp.route("/tickets", methods=["POST"])
def create_ticket():
    print("⚡️ Received POST /tickets")
    data = request.json
    user_id = data.get("user_id")
    user_email = data.get("email")
    message = data.get("message")

    if not user_id or not user_email or not message:
        return jsonify({"error": "user_id, email, and message are required"}), 400

    result = classify_and_draft(message)
    category = result["category"]
    draft = result["draft"]

    ticket = {
        "user_id": user_id,
        "email": user_email,
        "message": message,
        "category": category,
        "draft_response": draft,
        "status": "open",
        "created_at": datetime.datetime.utcnow(),
        "final_response": None,
        "assigned_to": None
    }

    inserted = db.tickets.insert_one(ticket)

    send_ticket_confirmation(user_email, str(inserted.inserted_id), category, message)

    return jsonify({
        "ticket_id": str(inserted.inserted_id),
        "category": category,
        "status": "open"
    }), 201

@tickets_bp.route("/users/<user_id>/tickets", methods=["GET"])
def get_user_tickets(user_id):
    try:
        tickets = list(db.tickets.find({"user_id": user_id}))
        for ticket in tickets:
            ticket["_id"] = str(ticket["_id"])
            ticket["created_at"] = ticket["created_at"].isoformat()
        return jsonify(tickets), 200
    except Exception as e:
        print("Error fetching tickets:", e)
        return jsonify({"error": "Failed to fetch tickets"}), 500


@tickets_bp.route("/tickets/all", methods=["GET"])
def get_all_tickets():
    try:
        tickets = list(db.tickets.find())
        for ticket in tickets:
            ticket["_id"] = str(ticket["_id"])
            ticket["created_at"] = ticket["created_at"].isoformat()
        return jsonify(tickets), 200
    except Exception as e:
        print("Error fetching all tickets:", e)
        return jsonify({"error": "Failed to fetch tickets"}), 500

from bson import ObjectId

from bson import ObjectId
from email_service import send_ticket_resolution_email

@tickets_bp.route("/tickets/<ticket_id>/response", methods=["POST"])
def respond_to_ticket(ticket_id):
    data = request.json
    responder = data.get("responder")  # IT member email or ID
    response_text = data.get("response")

    if not responder or not response_text:
        return jsonify({"error": "responder and response are required"}), 400

    # Check if the ticket exists and is open
    ticket = db.tickets.find_one({"_id": ObjectId(ticket_id), "status": "open"})
    if not ticket:
        return jsonify({"error": "Ticket already resolved or not found"}), 409

    # Update the ticket
    db.tickets.update_one(
        {"_id": ObjectId(ticket_id)},
        {
            "$set": {
                "final_response": response_text,
                "status": "resolved",
                "assigned_to": responder
            }
        }
    )

    # Send email if available
    if "email" in ticket:
        try:
            send_ticket_resolution_email(ticket["email"], ticket_id, response_text)
        except Exception as e:
            print("❌ Failed to send email notification:", e)
    else:
        print(f"⚠️ Ticket {ticket_id} does not have an 'email' field — skipping email notification.")

    # Return the updated ticket
    updated_ticket = db.tickets.find_one({"_id": ObjectId(ticket_id)})
    updated_ticket["_id"] = str(updated_ticket["_id"])
    updated_ticket["created_at"] = updated_ticket["created_at"].isoformat()

    return jsonify({
        "message": "Response submitted",
        "ticket": updated_ticket
    }), 200