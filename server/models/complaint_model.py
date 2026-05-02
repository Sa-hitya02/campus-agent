from datetime import datetime
from bson import ObjectId

# MongoDB collection name
COLLECTION = "complaints"

def create_complaint_doc(student_name: str, student_id: str, raw_text: str, agent_result: dict) -> dict:
    """Build the complaint document to insert into MongoDB."""
    return {
        "student_name": student_name,
        "student_id": student_id,
        "raw_text": raw_text,
        "category": agent_result.get("category"),
        "priority": agent_result.get("priority"),
        "department": agent_result.get("department"),
        "response": agent_result.get("response"),
        "sentiment": agent_result.get("sentiment"),
        "keywords": agent_result.get("keywords", []),
        "status": "open",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

def serialize(doc: dict) -> dict:
    """Convert MongoDB document to JSON-serializable dict."""
    doc["_id"] = str(doc["_id"])
    if "created_at" in doc:
        doc["created_at"] = doc["created_at"].isoformat()
    if "updated_at" in doc:
        doc["updated_at"] = doc["updated_at"].isoformat()
    return doc
