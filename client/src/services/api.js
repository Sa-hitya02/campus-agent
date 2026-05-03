const BASE_URL = "https://sahitya02.pythonanywhere.com/api/complaints";

const handleResponse = async (res) => {
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
};

export const submitComplaint = (payload) =>
  fetch(`${BASE_URL}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).then(handleResponse);

export const getAllComplaints = () =>
  fetch(`${BASE_URL}/all`).then(handleResponse);

export const getComplaint = (id) =>
  fetch(`${BASE_URL}/${id}`).then(handleResponse);

export const updateStatus = (id, status) =>
  fetch(`${BASE_URL}/${id}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  }).then(handleResponse);

export const getStats = () =>
  fetch(`${BASE_URL}/stats/summary`).then(handleResponse);