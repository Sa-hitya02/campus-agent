# 🧠 Smart Campus Complaint Agent

An AI-powered complaint management system for university campuses.  
Students submit complaints → Claude AI categorizes, prioritizes, assigns departments, and generates responses automatically.

---

## Architecture

```
Student → React Frontend → Flask API → AI Agent → MongoDB
                                          ↓
                              NLP → Categorize → Priority → Department → AI Response
```

---

## Quick Start

### 1. Clone & Setup Environment

```bash
git clone <your-repo>
cd campus-agent
```

### 2. Setup Backend

```bash
cd server

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# ✏️  Edit .env and fill in MONGO_URI and ANTHROPIC_API_KEY
```

### 3. Configure .env (IMPORTANT)

Open `server/.env` and fill in:

```
# MongoDB Atlas (recommended) or local MongoDB
MONGO_URI=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/campus_complaints

# Anthropic API Key — get from https://console.anthropic.com
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx

SECRET_KEY=any-random-string-here
```

### 4. Run Backend

```bash
cd server
python app.py
# Server runs on http://localhost:5000
```

### 5. Run Frontend

```bash
cd client
npm install
npm start
# React app runs on http://localhost:3000
```

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/complaints/submit` | Submit new complaint (runs AI agent) |
| GET | `/api/complaints/all` | Get all complaints |
| GET | `/api/complaints/:id` | Get single complaint |
| PATCH | `/api/complaints/:id/status` | Update complaint status |
| GET | `/api/complaints/stats/summary` | Get dashboard stats |

### Submit Example

```json
POST /api/complaints/submit
{
  "student_name": "Ravi Kumar",
  "student_id": "CS21B0042",
  "complaint_text": "The hostel bathroom taps have been leaking for 3 days. It is urgent."
}
```

### Response

```json
{
  "complaint_id": "668abc123...",
  "agent_result": {
    "category": "Hostel",
    "priority": "High",
    "department": "Hostel Administration Office",
    "sentiment": "negative",
    "keywords": ["hostel", "bathroom", "leaking", "urgent"],
    "response": "Dear Ravi Kumar, we have received your urgent complaint..."
  }
}
```

---

## AI Agent Pipeline

```
complaint_text
    │
    ▼
[NLP] extract_keywords() + analyze_sentiment()
    │
    ▼
[Claude AI] classify category → Infrastructure / Academic / Hostel / Safety / Admin / Sports
    │
    ▼
[Decision] assign_priority() → High / Medium / Low
           assign_department() → maps category → responsible office
    │
    ▼
[Claude AI] generate_response() → professional, empathetic reply
```

---

## Do I Need MongoDB Atlas?

**Local development**: Use `mongodb://localhost:27017/campus_complaints` (no account needed, install MongoDB locally).

**Production / cloud**: Use MongoDB Atlas free tier:
1. Go to https://cloud.mongodb.com
2. Create free cluster
3. Create user + password
4. Get connection string → paste in `.env`

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, React Router |
| Backend | Flask 3, Flask-PyMongo |
| AI | Claude claude-sonnet-4-20250514 (Anthropic) |
| Database | MongoDB |
| NLP | Rule-based fallback + Claude AI |
