const BASE_URL = "https://campus-agent-8mil-fm10qikc1-sa-hitya02s-projects.vercel.app/api";

const handleResponse = async (res) => {
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
};

export const submitComplaint = (payload) =>
  fetch(`${BASE_URL}/complaints/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).then(handleResponse);

export const getAllComplaints = () =>
  fetch(`${BASE_URL}/complaints/all`).then(handleResponse);

export const getComplaint = (id) =>
  fetch(`${BASE_URL}/complaints/${id}`).then(handleResponse);

export const updateStatus = (id, status) =>
  fetch(`${BASE_URL}/complaints/${id}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  }).then(handleResponse);

export const getStats = () =>
  fetch(`${BASE_URL}/complaints/stats/summary`).then(handleResponse);
