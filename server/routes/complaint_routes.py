from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime

from agent.agent import ComplaintAgent
from models.complaint_model import create_complaint_doc, serialize, COLLECTION
from utils.db import get_db

complaint_bp = Blueprint("complaints", __name__)
agent = ComplaintAgent()


# ─── POST /api/complaints/submit ─────────────────────────────────────────────
@complaint_bp.route("/submit", methods=["POST"])
def submit_complaint():
    data = request.get_json()

    # Validate required fields
    required = ["student_name", "student_id", "complaint_text"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    student_name = data["student_name"].strip()
    student_id = data["student_id"].strip()
    complaint_text = data["complaint_text"].strip()

    if len(complaint_text) < 10:
        return jsonify({"error": "Complaint text is too short."}), 400

    # Run agent
    result = agent.process(student_name, student_id, complaint_text)

    # Save to MongoDB
    db = get_db()
    doc = create_complaint_doc(student_name, student_id, complaint_text, result)
    inserted = db[COLLECTION].insert_one(doc)
    doc["_id"] = str(inserted.inserted_id)

    return jsonify({
        "message": "Complaint submitted successfully",
        "complaint_id": str(inserted.inserted_id),
        "agent_result": result,
    }), 201


# ─── GET /api/complaints/all ──────────────────────────────────────────────────
@complaint_bp.route("/all", methods=["GET"])
def get_all_complaints():
    db = get_db()
    complaints = list(db[COLLECTION].find().sort("created_at", -1).limit(100))
    return jsonify([serialize(c) for c in complaints]), 200


# ─── GET /api/complaints/<id> ─────────────────────────────────────────────────
@complaint_bp.route("/<complaint_id>", methods=["GET"])
def get_complaint(complaint_id):
    try:
        db = get_db()
        doc = db[COLLECTION].find_one({"_id": ObjectId(complaint_id)})
        if not doc:
            return jsonify({"error": "Complaint not found"}), 404
        return jsonify(serialize(doc)), 200
    except Exception:
        return jsonify({"error": "Invalid complaint ID"}), 400


# ─── PATCH /api/complaints/<id>/status ───────────────────────────────────────
@complaint_bp.route("/<complaint_id>/status", methods=["PATCH"])
def update_status(complaint_id):
    data = request.get_json()
    new_status = data.get("status")
    valid = ["open", "in_progress", "resolved", "closed"]

    if new_status not in valid:
        return jsonify({"error": f"Status must be one of: {valid}"}), 400

    try:
        db = get_db()
        result = db[COLLECTION].update_one(
            {"_id": ObjectId(complaint_id)},
            {"$set": {"status": new_status, "updated_at": datetime.utcnow()}}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Complaint not found"}), 404
        return jsonify({"message": "Status updated", "status": new_status}), 200
    except Exception:
        return jsonify({"error": "Invalid complaint ID"}), 400


# ─── GET /api/complaints/stats/summary ───────────────────────────────────────
@complaint_bp.route("/stats/summary", methods=["GET"])
def get_stats():
    db = get_db()
    total = db[COLLECTION].count_documents({})
    by_category = list(db[COLLECTION].aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ]))
    by_priority = list(db[COLLECTION].aggregate([
        {"$group": {"_id": "$priority", "count": {"$sum": 1}}}
    ]))
    by_status = list(db[COLLECTION].aggregate([
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]))

    return jsonify({
        "total": total,
        "by_category": {d["_id"]: d["count"] for d in by_category},
        "by_priority": {d["_id"]: d["count"] for d in by_priority},
        "by_status": {d["_id"]: d["count"] for d in by_status},
    }), 200
