import anthropic
import json
import re
from flask import current_app

from agent.nlp import extract_keywords, analyze_sentiment, classify_category_fallback
from agent.decision import decide
from agent.response import generate_response


class ComplaintAgent:
    """
    🧠 Smart Campus Complaint Agent
    Pipeline: NLP → Categorize → Prioritize → Assign → Respond
    """

    def process(self, student_name: str, student_id: str, complaint_text: str) -> dict:
        print(f"\n🧠 Agent processing complaint from {student_name}...")

        # Step 1: NLP — Extract keywords + sentiment
        keywords = extract_keywords(complaint_text)
        sentiment = analyze_sentiment(complaint_text)
        print(f"  📝 Keywords: {keywords}")
        print(f"  💭 Sentiment: {sentiment}")

        # Step 2: AI Categorization (with fallback)
        category = self._ai_categorize(complaint_text)
        print(f"  🏷️  Category: {category}")

        # Step 3: Decision — Priority + Department
        priority, department = decide(category, complaint_text)
        print(f"  ⚡ Priority: {priority} | 🏢 Department: {department}")

        # Step 4: Generate Response
        response = generate_response(
            student_name=student_name,
            category=category,
            priority=priority,
            department=department,
            complaint_text=complaint_text,
            sentiment=sentiment,
        )
        print(f"  ✅ Response generated.")

        return {
            "category": category,
            "priority": priority,
            "department": department,
            "response": response,
            "sentiment": sentiment,
            "keywords": keywords,
        }

    def _ai_categorize(self, complaint_text: str) -> str:
        """Use Claude to classify the complaint category, fallback to rule-based."""
        try:
            api_key = current_app.config.get("ANTHROPIC_API_KEY")
            if not api_key or api_key == "your-anthropic-api-key-here":
                return classify_category_fallback(complaint_text)

            client = anthropic.Anthropic(api_key=api_key)

            prompt = f"""Classify this campus complaint into exactly ONE of these categories:
- Infrastructure
- Academic
- Hostel
- Safety & Security
- Administrative
- Sports & Facilities
- General

Complaint: "{complaint_text}"

Respond with ONLY a JSON object like: {{"category": "Infrastructure"}}
No explanation, no extra text."""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )

            raw = message.content[0].text.strip()
            # Strip markdown fences if present
            raw = re.sub(r"```[a-z]*", "", raw).strip("` \n")
            data = json.loads(raw)
            return data.get("category", classify_category_fallback(complaint_text))

        except Exception as e:
            print(f"⚠️  AI categorization failed: {e}, using fallback.")
            return classify_category_fallback(complaint_text)
