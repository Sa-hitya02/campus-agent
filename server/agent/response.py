import anthropic
import os
from flask import current_app


def generate_response(
    student_name: str,
    category: str,
    priority: str,
    department: str,
    complaint_text: str,
    sentiment: str,
) -> str:
    """
    Use Claude AI to generate a professional, empathetic response to the student.
    Falls back to a template response if API call fails.
    """
    try:
        api_key = current_app.config.get("ANTHROPIC_API_KEY")
        if not api_key or api_key == "your-anthropic-api-key-here":
            return _template_response(student_name, category, priority, department)

        client = anthropic.Anthropic(api_key=api_key)

        prompt = f"""You are a professional and empathetic student affairs officer at a university campus.
A student has submitted a complaint. Write a formal, warm, and helpful acknowledgment response.

Student Name: {student_name}
Complaint Category: {category}
Priority Level: {priority}
Assigned Department: {department}
Student Sentiment: {sentiment}
Complaint Text: {complaint_text}

Guidelines:
- Address the student by name
- Acknowledge their specific issue
- Mention the department handling it
- Give a realistic resolution timeframe based on priority:
  * High priority → within 24 hours
  * Medium priority → within 3-5 working days
  * Low priority → within 7-10 working days
- Be professional but warm
- End with assurance and support contact
- Keep response to 4-6 sentences
- Do NOT use bullet points, just clean paragraphs"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()

    except Exception as e:
        print(f"⚠️  Claude API error: {e}")
        return _template_response(student_name, category, priority, department)


def _template_response(student_name: str, category: str, priority: str, department: str) -> str:
    """Fallback template when AI is unavailable."""
    timeframes = {"High": "24 hours", "Medium": "3–5 working days", "Low": "7–10 working days"}
    timeframe = timeframes.get(priority, "5 working days")

    return (
        f"Dear {student_name}, thank you for bringing this {category.lower()} concern to our attention. "
        f"Your complaint has been received and classified as {priority.lower()} priority. "
        f"It has been forwarded to the {department}, who will review and address it within {timeframe}. "
        f"We sincerely apologize for any inconvenience caused and appreciate your patience. "
        f"For urgent follow-up, please contact the Student Grievance Cell. "
        f"Your complaint reference number has been generated for tracking purposes."
    )
