import React, { useState } from "react";
import { submitComplaint } from "../services/api";
import "./SubmitPage.css";

const SubmitPage = () => {
  const [form, setForm] = useState({
    student_name: "",
    student_id: "",
    complaint_text: "",
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const data = await submitComplaint(form);
      setResult(data);
      setForm({ student_name: "", student_id: "", complaint_text: "" });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const PRIORITY_COLORS = { High: "#ef4444", Medium: "#f59e0b", Low: "#22c55e" };

  return (
    <div className="submit-page">
      <div className="submit-card">
        <div className="submit-header">
          <span className="brain-icon">🧠</span>
          <h1>Smart Campus Complaint</h1>
          <p>Our AI agent will categorize, prioritize, and route your complaint instantly.</p>
        </div>

        <form onSubmit={handleSubmit} className="complaint-form">
          <div className="form-row">
            <div className="form-group">
              <label>Full Name</label>
              <input
                name="student_name"
                value={form.student_name}
                onChange={handleChange}
                placeholder="e.g. Ravi Kumar"
                required
              />
            </div>
            <div className="form-group">
              <label>Student ID</label>
              <input
                name="student_id"
                value={form.student_id}
                onChange={handleChange}
                placeholder="e.g. CS21B0042"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Describe Your Complaint</label>
            <textarea
              name="complaint_text"
              value={form.complaint_text}
              onChange={handleChange}
              placeholder="Describe your issue in detail — the more specific, the better our AI can help you..."
              rows={5}
              required
              minLength={10}
            />
            <span className="char-count">{form.complaint_text.length} characters</span>
          </div>

          {error && <div className="error-box">⚠️ {error}</div>}

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? (
              <><span className="spinner" /> Agent is analyzing...</>
            ) : (
              "Submit to AI Agent →"
            )}
          </button>
        </form>

        {result && (
          <div className="result-card">
            <div className="result-header">
              <span>✅</span>
              <h2>Complaint Processed Successfully</h2>
              <code className="complaint-id">ID: {result.complaint_id}</code>
            </div>

            <div className="agent-tags">
              <span className="tag category">{result.agent_result.category}</span>
              <span
                className="tag priority"
                style={{ background: PRIORITY_COLORS[result.agent_result.priority] + "22",
                         color: PRIORITY_COLORS[result.agent_result.priority],
                         borderColor: PRIORITY_COLORS[result.agent_result.priority] }}
              >
                {result.agent_result.priority} Priority
              </span>
              <span className="tag sentiment">{result.agent_result.sentiment} sentiment</span>
            </div>

            <div className="department-box">
              <span className="dept-label">🏢 Assigned To</span>
              <span className="dept-name">{result.agent_result.department}</span>
            </div>

            {result.agent_result.keywords?.length > 0 && (
              <div className="keywords">
                {result.agent_result.keywords.map((k) => (
                  <span key={k} className="keyword-chip">#{k}</span>
                ))}
              </div>
            )}

            <div className="ai-response">
              <p className="response-label">📨 AI Response to Student</p>
              <p>{result.agent_result.response}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SubmitPage;
