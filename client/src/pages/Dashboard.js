import React, { useEffect, useState } from "react";
import { getAllComplaints, getStats, updateStatus } from "../services/api";
import "./Dashboard.css";

const PRIORITY_COLOR = { High: "#ef4444", Medium: "#f59e0b", Low: "#22c55e" };
const STATUS_OPTIONS = ["open", "in_progress", "resolved", "closed"];

const Dashboard = () => {
  const [complaints, setComplaints] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState(null);

  const fetchData = async () => {
    try {
      const [c, s] = await Promise.all([getAllComplaints(), getStats()]);
      setComplaints(c);
      setStats(s);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  const handleStatusChange = async (id, status) => {
    await updateStatus(id, status);
    fetchData();
    if (selected?._id === id) setSelected({ ...selected, status });
  };

  const filtered = filter === "all"
    ? complaints
    : complaints.filter((c) => c.priority?.toLowerCase() === filter || c.status === filter);

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="sidebar-logo">🧠 Campus Agent</div>

        {stats && (
          <div className="stat-section">
            <div className="stat-item">
              <span className="stat-num">{stats.total}</span>
              <span className="stat-label">Total Complaints</span>
            </div>
            {Object.entries(stats.by_priority || {}).map(([p, n]) => (
              <div className="stat-item" key={p}>
                <span className="stat-num" style={{ color: PRIORITY_COLOR[p] }}>{n}</span>
                <span className="stat-label">{p} Priority</span>
              </div>
            ))}
          </div>
        )}

        <div className="filter-section">
          <p className="filter-label">Filter</p>
          {["all", "High", "Medium", "Low", "open", "resolved"].map((f) => (
            <button
              key={f}
              className={`filter-btn ${filter === f ? "active" : ""}`}
              onClick={() => setFilter(f)}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </aside>

      <main className="main-panel">
        <div className="panel-header">
          <h1>Complaint Dashboard</h1>
          <button className="refresh-btn" onClick={fetchData}>⟳ Refresh</button>
        </div>

        {loading ? (
          <div className="loading">Loading complaints...</div>
        ) : filtered.length === 0 ? (
          <div className="empty">No complaints found.</div>
        ) : (
          <div className="complaint-grid">
            {filtered.map((c) => (
              <div
                key={c._id}
                className={`complaint-card ${selected?._id === c._id ? "selected" : ""}`}
                onClick={() => setSelected(c)}
              >
                <div className="card-top">
                  <span className="student-name">{c.student_name}</span>
                  <span className="student-id">{c.student_id}</span>
                </div>
                <p className="card-text">{c.raw_text?.slice(0, 90)}...</p>
                <div className="card-tags">
                  <span className="ctag cat">{c.category}</span>
                  <span
                    className="ctag pri"
                    style={{ color: PRIORITY_COLOR[c.priority], borderColor: PRIORITY_COLOR[c.priority] + "55" }}
                  >
                    {c.priority}
                  </span>
                  <span className={`ctag status-${c.status}`}>{c.status}</span>
                </div>
                <div className="card-date">{new Date(c.created_at).toLocaleString()}</div>
              </div>
            ))}
          </div>
        )}
      </main>

      {selected && (
        <div className="detail-panel">
          <button className="close-btn" onClick={() => setSelected(null)}>✕</button>
          <h2>{selected.student_name}</h2>
          <code>{selected.student_id}</code>

          <div className="detail-section">
            <p className="detail-label">Complaint</p>
            <p className="detail-text">{selected.raw_text}</p>
          </div>

          <div className="detail-row">
            <div>
              <p className="detail-label">Category</p>
              <p className="detail-value">{selected.category}</p>
            </div>
            <div>
              <p className="detail-label">Priority</p>
              <p className="detail-value" style={{ color: PRIORITY_COLOR[selected.priority] }}>
                {selected.priority}
              </p>
            </div>
            <div>
              <p className="detail-label">Sentiment</p>
              <p className="detail-value">{selected.sentiment}</p>
            </div>
          </div>

          <div className="detail-section">
            <p className="detail-label">Department</p>
            <p className="detail-value">{selected.department}</p>
          </div>

          <div className="detail-section">
            <p className="detail-label">AI Response</p>
            <p className="detail-text ai-resp">{selected.response}</p>
          </div>

          <div className="status-control">
            <p className="detail-label">Update Status</p>
            <div className="status-btns">
              {STATUS_OPTIONS.map((s) => (
                <button
                  key={s}
                  className={`status-opt ${selected.status === s ? "active" : ""}`}
                  onClick={() => handleStatusChange(selected._id, s)}
                >
                  {s.replace("_", " ")}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
