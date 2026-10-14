import { useCallback, useEffect, useState } from "react";

async function readResponse(response) {
  if (response.ok) {
    return response.status === 204 ? null : response.json();
  }

  let message = "Request failed";
  try {
    const payload = await response.json();
    message = payload.detail || message;
  } catch {
    // Keep the simple fallback when the server does not return JSON.
  }
  throw new Error(message);
}

function App() {
  const [resumes, setResumes] = useState([]);
  const [selectedIds, setSelectedIds] = useState(new Set());
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [uploadStatus, setUploadStatus] = useState({ message: "", error: false });
  const [questionStatus, setQuestionStatus] = useState({ message: "", error: false });
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);

  const loadResumes = useCallback(async () => {
    try {
      const data = await readResponse(await fetch("/api/resumes"));
      setResumes(data);
      setSelectedIds((current) => {
        const available = new Set(data.map((resume) => resume.resume_id));
        const kept = new Set([...current].filter((id) => available.has(id)));
        // Select newly loaded resumes by default.
        data.forEach((resume) => kept.add(resume.resume_id));
        return kept;
      });
    } catch (error) {
      setQuestionStatus({ message: error.message, error: true });
    }
  }, []);

  useEffect(() => {
    loadResumes();
  }, [loadResumes]);

  function toggleResume(id) {
    setSelectedIds((current) => {
      const next = new Set(current);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  async function uploadFiles(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const files = form.elements.files.files;
    const data = new FormData();
    for (const file of files) data.append("files", file);

    setUploading(true);
    setUploadStatus({ message: "Uploading, extracting text, and creating embeddings...", error: false });
    try {
      const payload = await readResponse(
        await fetch("/api/resumes", { method: "POST", body: data }),
      );
      setUploadStatus({ message: `Indexed ${payload.resumes.length} resume(s).`, error: false });
      form.reset();
      await loadResumes();
    } catch (error) {
      setUploadStatus({ message: error.message, error: true });
    } finally {
      setUploading(false);
    }
  }

  async function deleteResume(resume) {
    if (!window.confirm(`Delete ${resume.original_name}?`)) return;
    try {
      await readResponse(
        await fetch(`/api/resumes/${resume.resume_id}`, { method: "DELETE" }),
      );
      await loadResumes();
    } catch (error) {
      setQuestionStatus({ message: error.message, error: true });
    }
  }

  async function askQuestion(event) {
    event.preventDefault();
    if (!selectedIds.size) {
      setQuestionStatus({ message: "Select at least one resume.", error: true });
      return;
    }

    setAsking(true);
    setAnswer("");
    setSources([]);
    setQuestionStatus({ message: "Finding relevant resume sections and generating an answer...", error: false });
    try {
      const payload = await readResponse(
        await fetch("/api/questions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question, resume_ids: [...selectedIds] }),
        }),
      );
      setAnswer(payload.answer);
      setSources(payload.sources);
      setQuestionStatus({ message: "", error: false });
    } catch (error) {
      setQuestionStatus({ message: error.message, error: true });
    } finally {
      setAsking(false);
    }
  }

  return (
    <main className="layout">
      <header>
        <p className="eyebrow">RESUME RAG</p>
        <h1>Ask questions across resumes</h1>
        <p>Upload resumes, select candidates, and get answers grounded in their content.</p>
      </header>

      <section className="card">
        <h2>1. Upload resumes</h2>
        <form onSubmit={uploadFiles}>
          <input name="files" type="file" accept=".pdf,.docx,.txt" multiple required />
          <button type="submit" disabled={uploading}>Upload and index</button>
        </form>
        <Status value={uploadStatus} />
      </section>

      <section className="card">
        <div className="title-row">
          <h2>2. Select resumes</h2>
          <button className="secondary" type="button" onClick={loadResumes}>Refresh</button>
        </div>
        <div className="resume-list">
          {resumes.length === 0 && <p>No resumes uploaded yet.</p>}
          {resumes.map((resume) => (
            <div className="resume-row" key={resume.resume_id}>
              <label className="resume-label">
                <input
                  type="checkbox"
                  checked={selectedIds.has(resume.resume_id)}
                  onChange={() => toggleResume(resume.resume_id)}
                />
                <span>
                  <strong>{resume.original_name}</strong>
                  <span className="resume-meta"> · {resume.chunk_count} chunks</span>
                </span>
              </label>
              <button className="danger" type="button" onClick={() => deleteResume(resume)}>Delete</button>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <h2>3. Ask a question</h2>
        <form onSubmit={askQuestion}>
          <textarea
            rows="4"
            placeholder="Which selected candidates have FastAPI experience?"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            required
          />
          <button type="submit" disabled={asking}>Ask selected resumes</button>
        </form>
        <Status value={questionStatus} />
        {answer && <div className="answer">{answer}</div>}
        <div className="sources">
          {sources.map((source, index) => (
            <details className="source" key={`${source.resume_id}-${source.chunk_number}-${index}`}>
              <summary>
                {source.resume_name} · chunk {source.chunk_number} · score {source.score}
              </summary>
              <p>{source.text}</p>
            </details>
          ))}
        </div>
      </section>
    </main>
  );
}

function Status({ value }) {
  return <p className={`status${value.error ? " error" : ""}`}>{value.message}</p>;
}

export default App;
