import axios from "axios";

export const api = axios.create({ baseURL: "/api", timeout: 120_000 });

api.interceptors.response.use(
  (response) => response,
  (error) =>
    Promise.reject(
      new Error(
        error.response?.data?.detail || error.message || "Request failed",
      ),
    ),
);

export async function listResumes() {
  return (await api.get("/resumes")).data;
}

export async function uploadResumes(files) {
  const body = new FormData();
  for (const file of files) body.append("files", file);
  return (await api.post("/resumes", body)).data;
}

export async function removeResume(id) {
  await api.delete(`/resumes/${id}`);
}

// Axios buffers browser responses, so the browser stream API is used only here.
export async function streamQuestion(payload, onEvent, signal) {
  const response = await fetch("/api/questions/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Could not answer the question");
  }
  if (!response.body)
    throw new Error("Streaming is unsupported by this browser");

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { done, value } = await reader.read();
    buffer += decoder.decode(value || new Uint8Array(), { stream: !done });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";
    for (const line of lines) if (line.trim()) onEvent(JSON.parse(line));
    if (done) break;
  }
}
